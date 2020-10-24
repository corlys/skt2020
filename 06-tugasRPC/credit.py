import zerorpc
import threading

class creditRPC(object):
    points = 0
    

    def __init__(self):
        self.conn = zerorpc.Client()
        self.conn.connect("tcp://127.0.0.1:4243")

    def hello(self, name):
        return "Hello, %s" % name

    def test(self):
        global points
        points  =- 100
        return points

    def get_status(self, amount):
        return self.conn.checkSaldo(amount)

    def beli_pulsa(self, ammount):
        status = self.get_status(ammount)
        if status:
            return "Berhasil Beli Pulsa"
        else:
            return "Tidak berhasil beli pulsa"

    

try :
    def buyer_conn():
        s = zerorpc.Server(creditRPC())
        s.bind("tcp://0.0.0.0:4242")
        s.run()
    clientThread = threading.Thread(target=buyer_conn, args=())
    clientThread.start()
    
except KeyboardInterrupt:
    print("Keluar")