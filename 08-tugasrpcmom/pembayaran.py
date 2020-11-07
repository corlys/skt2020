import zerorpc

class paymentRPC(object):
    saldo = 10000

    def checkSaldo(self, ammount):
        print('hellio ')
        print(ammount < self.saldo)
        return (ammount < self.saldo)

    def hello(self, test):
        return "OKE %s" % test


try :
    s = zerorpc.Server(paymentRPC())
    s.bind("tcp://0.0.0.0:4243")
    s.run()
except KeyboardInterrupt:
    print("Keluar")