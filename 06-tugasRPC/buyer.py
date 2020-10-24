import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
while True:
    data = int(input("masukkan ammount pulsa : "))
    print(c.beli_pulsa(data))