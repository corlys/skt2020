# Muhammad Naufal Dzakie - 175150207111016
# Ray Wirawan Z. King - 175150200111024


import zerorpc
import gevent
import sys
from datetime import datetime


class State():
    def __init__(self):
        self.clock = datetime.today()
        self.coordinator = 0
        self.state = "Normal"
        self.desc = None
        self.halt = -1
        self.Up = []

class Bully():
    def __init__(self, addr, config_file="list_server"):
        
        self.nodestate = State()
        
        self.servers = []

        self.addr = addr

        self.conn = []

        self.check_servers_greenlet = None
        
        f = open(config_file, 'r')
        for line in f.readlines():
            line = line.rstrip()
            self.servers.append(line)
            # print("server  disimpan")

        # print ('My addr: %s' % self.addr)
        # print ('Server list: %s' % (str(self.servers)))

        for index, server in enumerate(self.servers):
            if server == self.addr:
                # print('addr sama')
                self.index = index
                self.conn.append(self)
            else :
                # print("addr beda")
                connrpc = zerorpc.Client(timeout=2)
                # if server != self.addr:
                connrpc.connect('tcp://' +server)
                self.conn.append(connrpc)

    def readfile_again(self, config_file="server_config"):
        
        # self.conn = []
        # self.servers = []
        
        f = open(config_file, 'r')
        for line in f.readlines():
            line = line.rstrip()
            for i, server in enumerate(self.servers):
                if server not in self.servers:
                    self.servers.append(line)

        print(self.servers)
            # print("server  disimpan")
            
        for index, server in enumerate(self.servers):
            if server == self.addr:
                if server not in self.servers:
                    self.index = index
                    self.conn.append(self)
            else :
                if server not in self.servers: 
                    connrpc = zerorpc.Client(timeout=2)
                    connrpc.connect("tcp://" +server)
                    self.conn.append(connrpc)

    def election(self):
        print ('Check the states of higher priority nodes:')
        print(self.servers)
        for i, server in enumerate(self.servers[self.index + 1:]):
            # print(self.index)
            # print(i)
            # print(server)
            try:
                self.conn[self.index + 1 + i].are_you_there()
                # print('nasi goreng')
                print(self.check_servers_greenlet)
                if self.check_servers_greenlet is None:
                    # print('nasi pecel')
                    self.nodestate.coordinator = self.index + 1 + i
                    # print(self.nodestate.coordinator)
                    self.nodestate.state = 'Normal'
                    self.check_servers_greenlet = self.pool.spawn(self.check())
                return
            except zerorpc.TimeoutExpired:
                # print('timeout check the states')
                print ('%s Timeout!' % server)

        print ('halt all lower priority nodes including this node:')
        self.halt(self.index)
        self.nodestate.state = 'Election'
        self.nodestate.halt = self.index
        self.nodestate.Up = []
        for i, server in enumerate(self.servers[self.index::-1]):
            try:
                self.conn[i].halt(self.index)
            except zerorpc.TimeoutExpired:
                # print ('timeout halt lower priority')
                print ('%s Timeout!' % server)
                continue
            self.nodestate.Up.append(self.conn[i])

        # reached 'election point',inform nodes of new coordinator
        print ('inform nodes of new coordinator:')
        self.nodestate.coordinator = self.index
        self.nodestate.state = 'Reorganization'
        for j in self.nodestate.Up:
            try:
                j.new_coordinator(self.index)
            except zerorpc.TimeoutExpired:
                print ('Timeout! Election will be restarted.')
                self.election()
                return

        # Reorganization
        for j in self.nodestate.Up:
            try:
                j.ready(self.index, self.nodestate.desc)
            except zerorpc.TimeoutExpired:
                print('Timeout Reorg')
                print ('Timeout!')
                self.election()
                return

        self.nodestate.state = 'Normal'
        print ('[%s] Starting ZeroRPC Server' % self.servers[self.index])
        print("starting zeroRpc dari election")
        self.check_servers_greenlet = self.pool.spawn(self.check())
        # print('ni woooooouuuuuiiiii')
        # print(self.check_servers_greenlet)
        # print(type(self.check_servers_greenlet))

    def are_you_normal(self):
        if self.nodestate.state == 'Normal':
            return True
        else:
            return False

    def halt(self, j):
        self.nodestate.state = 'Election'
        self.nodestate.halt = j

    def new_coordinator(self, j):
        print ('call new_coordinator')
        if self.nodestate.halt == j and self.nodestate.state == 'Election':
            self.nodestate.coordinator = j
            self.nodestate.state = 'Reorganization'

    def ready(self, j, x=None):
        print ('call ready')
        if self.nodestate.coordinator == j and self.nodestate.state == "Reorganization":
            self.nodestate.desc = x
            self.nodestate.state = 'Normal'

    def check(self):
        while True:
            gevent.sleep(5)
            if self.nodestate.state == 'Normal' and self.nodestate.coordinator == self.index:
                for i, server in enumerate(self.servers):
                    if i != self.index:
                        try:
                            # self.readfile_again()
                            if self.conn[i] not in self.nodestate.Up:
                                self.nodestate.Up.append(self.conn[i])
                            ans = self.conn[i].are_you_normal()
                            print ('%s : are_you_normal = %s' % (server, ans))
                            # print(self.pool)  
                        except zerorpc.TimeoutExpired:
                            # print('timeout di check')
                            print ('%s Timeout!' % server)
                            self.nodestate.Up = []
                            for j, liveserv in enumerate(self.servers):
                                if liveserv != server:
                                    self.nodestate.Up.append(self.conn[j])
                            continue

                        if not ans:
                            self.election()
                            return
                self.syclock()
            elif self.nodestate.state == 'Normal' and self.nodestate.coordinator != self.index:
                print ('check coordinator\'s state')
                try:
                    result = self.conn[self.nodestate.coordinator].are_you_there()
                    print ('%s : are_you_there = %s' % (self.servers[self.nodestate.coordinator], result))
                except zerorpc.TimeoutExpired:
                    print ('coordinator down, rasie eleciton.')
                    self.timeout()

    def are_you_there(self):
        return True
    
    def timeout(self):
        if self.nodestate.state == 'Normal' or self.nodestate.state == 'Reorganization':
            try:
                self.conn[self.nodestate.coordinator].are_you_there()
            except zerorpc.TimeoutExpired:
                print ('%s Timeout!' % self.servers[self.nodestate.coordinator])
                self.election()
        else:
            self.election()

    def what_time(self):
        seconds = self.nodestate.clock.timestamp()
        return seconds

    def set_time(self, seconds):
        self.nodestate.clock = datetime.fromtimestamp(seconds)
        newtime = self.nodestate.clock.strftime("%A, %B %d, %Y %I:%M:%S")
        print('newtime is '+newtime)
        return seconds

    def syclock(self):
        if self.nodestate.state == 'Normal' and self.nodestate.coordinator == self.index:
            self.nodestate.clock = datetime.today()
            timepool = self.nodestate.clock.timestamp()
            for i, server in enumerate(self.servers):
                if self.index != i:
                    try:
                        ans = self.conn[i].what_time()
                        # print('ngecek time di orang lain')
                        timepool = timepool + ans
                    except zerorpc.TimeoutExpired:
                        print ('%s syclock Timeout!' % server)
                        continue
            # print('masuk tengah syclock')
            print(len(self.nodestate.Up))
            timepool = timepool / len(self.nodestate.Up)
            for i, server in enumerate(self.servers):
                if self.index != i:
                    try:
                        # print('masuk bagi2 waktu')
                        ans = self.conn[i].set_time(timepool)
                    except zerorpc.TimeoutExpired:
                        print ('%s syclock Timeout!' % server)
                        continue
            newtime = datetime.fromtimestamp(timepool).strftime("%A, %B %d, %Y %I:%M:%S")
            print('newtime is '+newtime)

    def recovery(self):
        self.nodestate.halt = -1
        self.election()

    def start(self):
        self.pool = gevent.pool.Group()
        self.recovery_greenlet = self.pool.spawn(self.recovery)

def main():
    addr = sys.argv[1]
    print(addr)
    bully = Bully(addr)
    s = zerorpc.Server(bully)
    s.bind("tcp://"+addr)
    bully.start()
    s.run()

if __name__ == "__main__" :
    main()

        





    

    