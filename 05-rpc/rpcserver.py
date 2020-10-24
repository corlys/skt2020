import zerorpc

class HelloRPC(object):
    points = 0

    def hello(self, name):
        return "Hello, %s" % name

    def test(self):
        global points
        points  =- 100
        return points
try :
    s = zerorpc.Server(HelloRPC())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
except KeyboardInterrupt:
    print("Keluar")