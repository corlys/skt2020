import zerorpc

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name
try :
    s = zerorpc.Server(HelloRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
except KeyboardInterrupt:
    print("Keluar")