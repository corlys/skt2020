import zerorpc
import threading
import paho.mqtt.client as mqtt

class creditRPC(object):
    

    def __init__(self):
        self.conn = zerorpc.Client()
        self.conn.connect("tcp://127.0.0.1:4243")
        self.client = mqtt.Client(client_id="pub1", clean_session=False)
        self.client.connect("127.0.0.1", port=1883)

    def get_status(self, amount):
        return self.conn.checkSaldo(amount)

    def beli_pulsa(self, ammount):
        status = self.get_status(ammount)
        if status:
            self.client.publish("/status/1", payload="Transaksi Berhasil", qos=1)
        else:
            self.client.publish("/status/1", payload="Transaksi Tidak Berhasil", qos=1)

    

try :
    def buyer_conn():
        s = zerorpc.Server(creditRPC())
        s.bind("tcp://0.0.0.0:4242")
        s.run()
    clientThread = threading.Thread(target=buyer_conn, args=())
    clientThread.start()
    
except KeyboardInterrupt:
    print("Keluar")