import zerorpc
import gevent
import sys
from datetime import datetime


class StateVector():
    def __init__(self):
        self.clock = datetime.today()
        # state of the node
        # [Down, Election, Reorganization, Normal]
        self.s = 'Normal'
        # coordinator of the node
        self.c = 0
        # description of task
        self.d = None
        # the node recently makes this node halt
        self.h = -1
        # list of nodes which this node believes to be in operation
        self.Up = []


class Bully():
    def __init__(self, addr, config_file='server_config'):
        self.S = StateVector()
        self.S.s = 'Normal'

        self.check_servers_greenlet = None

        self.addr = addr

        self.servers = []
        f = open(config_file, 'r')
        for line in f.readlines():
            line = line.rstrip()
            self.servers.append(line)
        print ('My addr: %s' % self.addr)
        print ('Server list: %s' % (str(self.servers)))

        self.n = len(self.servers)

        self.connections = []

        for i, server in enumerate(self.servers):
            if server == self.addr:
                self.i = i
                self.connections.append(self)
            else:
                c = zerorpc.Client(timeout=2)
                c.connect('tcp://' + server)
                self.connections.append(c)

    def are_you_there(self):
        return True

    def are_you_normal(self):
        if self.S.s == 'Normal':
            return True
        else:
            return False

    def halt(self, j):
        self.S.s = 'Election'
        self.S.h = j

    def new_coordinator(self, j):
        print ('call new_coordinator')
        if self.S.h == j and self.S.s == 'Election':
            self.S.c = j
            self.S.s = 'Reorganization'

    def ready(self, j, x=None):
        print ('call ready')
        if self.S.c == j and self.S.s == "Reorganization":
            self.S.d = x
            self.S.s = 'Normal'

    def election(self):
        print ('Check the states of higher priority nodes:')
        print(self.servers)
        for i, server in enumerate(self.servers[self.i + 1:]):
            print(self.i)
            print(i)
            print(server)
            try:
                self.connections[self.i + 1 + i].are_you_there()
                print('nasi goreng')
                print(self.check_servers_greenlet)
                if self.check_servers_greenlet is None:
                    print('nasi pecel')
                    self.S.c = self.i + 1 + i
                    print(self.S.c)
                    self.S.s = 'Normal'
                    self.check_servers_greenlet = self.pool.spawn(self.check())
                return
            except zerorpc.TimeoutExpired:
                print('timeout check the states')
                print ('%s Timeout!' % server)

        print ('halt all lower priority nodes including this node:')
        self.halt(self.i)
        self.S.s = 'Election'
        self.S.h = self.i
        self.S.Up = []
        for i, server in enumerate(self.servers[self.i::-1]):
            try:
                self.connections[i].halt(self.i)
            except zerorpc.TimeoutExpired:
                print ('timeout halt lower priority')
                print ('%s Timeout!' % server)
                continue
            self.S.Up.append(self.connections[i])

        # reached 'election point',inform nodes of new coordinator
        print ('inform nodes of new coordinator:')
        self.S.c = self.i
        self.S.s = 'Reorganization'
        for j in self.S.Up:
            try:
                j.new_coordinator(self.i)
            except zerorpc.TimeoutExpired:
                print ('Timeout! Election will be restarted.')
                self.election()
                return

        # Reorganization
        for j in self.S.Up:
            try:
                j.ready(self.i, self.S.d)
            except zerorpc.TimeoutExpired:
                print('Timeout Reorg')
                print ('Timeout!')
                self.election()
                return

        self.S.s = 'Normal'
        print ('[%s] Starting ZeroRPC Server' % self.servers[self.i])
        print("starting zeroRpc dari election")
        self.check_servers_greenlet = self.pool.spawn(self.check())
        # print('ni woooooouuuuuiiiii')
        # print(self.check_servers_greenlet)
        # print(type(self.check_servers_greenlet))

    def recovery(self):
        self.S.h = -1
        self.election()

    def check(self):
        while True:
            gevent.sleep(5)
            if self.S.s == 'Normal' and self.S.c == self.i:
                for i, server in enumerate(self.servers):
                    if i != self.i:
                        try:
                            ans = self.connections[i].are_you_normal()
                            print ('%s : are_you_normal = %s' % (server, ans))
                            # print(self.pool)
                            self.syclock()
                        except zerorpc.TimeoutExpired:
                            print('timeout di check')
                            print ('%s Timeout!' % server)
                            continue

                        if not ans:
                            self.election()
                            return
            elif self.S.s == 'Normal' and self.S.c != self.i:
                print ('check coordinator\'s state')
                try:
                    result = self.connections[self.S.c].are_you_there()
                    print ('%s : are_you_there = %s' % (self.servers[self.S.c], result))
                except zerorpc.TimeoutExpired:
                    print ('coordinator down, rasie eleciton.')
                    self.timeout()

    def what_time(self):
        seconds = self.S.clock.timestamp()
        return seconds

    def set_time(self, seconds):
        print(seconds)
        self.S.clock = datetime.fromtimestamp(seconds)
        newtime = self.S.clock.strftime("%A, %B %d, %Y %I:%M:%S")
        print('newtime is '+newtime)
        return seconds

    def syclock(self):
        if self.S.s == 'Normal' and self.S.c == self.i:
            self.S.clock = datetime.today()
            timepool = self.S.clock.timestamp()
            for i, server in enumerate(self.servers):
                if self.i != i:
                    ans = self.connections[i].what_time()
                    print('ngecek time di orang lain')
                    timepool = timepool + ans
            print('masuk tengah syclock')
            timepool = timepool / len(self.servers)
            for i, server in enumerate(self.servers):
                if self.i != i:
                    print('masuk bagi2 waktu')
                    ans = self.connections[i].set_time(timepool)
            newtime = datetime.fromtimestamp(timepool).strftime("%A, %B %d, %Y %I:%M:%S")
            print('newtime is '+newtime)

    def timeout(self):
        if self.S.s == 'Normal' or self.S.s == 'Reorganization':
            try:
                self.connections[self.S.c].are_you_there()
            except zerorpc.TimeoutExpired:
                print('timeout di timeout')
                print ('%s Timeout!' % self.servers[self.S.c])
                self.election()
        else:
            self.election()

    def start(self):
        self.pool = gevent.pool.Group()
        self.recovery_greenlet = self.pool.spawn(self.recovery)


def main():
    addr = sys.argv[1]
    bully = Bully(addr)
    s = zerorpc.Server(bully)
    s.bind('tcp://' + addr)
    bully.start()
    # Start server
    print ('[%s] Starting ZeroRPC Server' % addr)
    print("starting zeroRpc dari main")
    s.run()


if __name__ == '__main__':
    main()