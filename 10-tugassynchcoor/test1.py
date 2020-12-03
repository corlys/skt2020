import datetime


class Test():
    def __init__(self):
        self.list = ['127.0.0.1:4000', '127.0.0.1:4001', '127.0.0.1:4002']

    def main(self):
        # time = datetime.datetime.today()
        # print(time)
        for i, server in enumerate(self.list):
            print(i)
            print(server)
        
t = Test()
t.main()