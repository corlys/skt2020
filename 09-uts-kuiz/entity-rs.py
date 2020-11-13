# implementasi server di sini
import zerorpc
import threading
import paho.mqtt.client as mqtt
import json

nama_rs = input("Nama Rumah Sakit : ")
server_port = input("Port RPC Server Rumah Sakit : ")

class rumahSakitRPC(object):

    dictionaryData = []

    

    def on_message(self, client, obj, msg):
        # _payload = json.loads(msg.payload)
        
        # self.dictionaryData.append(_payload)
        # print(self.dictionaryData)

        _payload = json.loads(msg.payload)
        for dick in _payload:
            self.dictionaryData.append(dick)
        print(self.dictionaryData)


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def __init__(self):
        self.conn = zerorpc.Client()
        self.conn.connect("tcp://127.0.0.1:"+server_port)
        self.client = mqtt.Client(client_id=nama_rs, clean_session=False)
        self.client.connect("127.0.0.1", port=1883)
        # Subscribe ke salah satu topik
        self.client.subscribe("patientdata", qos=1)
        # Daftarkan fungsi callback
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        clientThread = threading.Thread(target=self.handle_thread, args=(self.client,))
        clientThread.start()

    def sendData(self, nik, nama, alamat, penyakit):
        _nik = nik
        _nama = nama
        _alamat = alamat
        _penyakit = penyakit
        newDict = {
            "nik" : _nik,
            "nama" : _nama,
            "alamat": _alamat,
            "penyakit" : _penyakit
        }
        
        self.dictionaryData.append(newDict)

        self.client.publish("patientdata", payload=json.dumps(self.dictionaryData), qos=1) 
        return True

    def getData(self, nik):
        for dic in self.dictionaryData:
            for key in dic:
                if(nik == dic[key]):
                    return dic
    def handle_thread(self, client):
        try :
            # Buat infinite loop supaya subscriber tidak mati
            self.client.loop_forever()
        except KeyboardInterrupt :
            print("Subscriber mati")


try:
    s = zerorpc.Server(rumahSakitRPC())
    s.bind("tcp://0.0.0.0:"+server_port)
    s.run()

    # rs = rumahSakitRPC()
except KeyboardInterrupt:
    print("Keluar")
    exit()
