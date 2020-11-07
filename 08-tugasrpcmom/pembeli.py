import zerorpc
import threading
# import library paho mqtt
import paho.mqtt.client as mqtt

# inisiasi client mqtt
client = mqtt.Client(client_id="sub1", clean_session=False)

# Koneksikan ke broker
client.connect("127.0.0.1", port=1883)

# Subscribe ke salah satu topik
client.subscribe("/status/1", qos=1)

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")


# Buat fungsi untuk menghandle message yang masuk
def on_message(client, obj, msg):
    print(msg.payload)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Daftarkan fungsi callback
client.on_connect = on_connect
client.on_message = on_message

def handle_thread(client):
    try :
        # Buat infinite loop supaya subscriber tidak mati
        client.loop_forever()
    except KeyboardInterrupt :
        print("Subscriber mati")

subsThread = threading.Thread(target=handle_thread, args=(client,))
subsThread.start()

while True:
    data = int(input("masukkan ammount pulsa : "))
    c.beli_pulsa(data)

