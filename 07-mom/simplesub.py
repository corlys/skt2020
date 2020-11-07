# import library paho mqtt
import paho.mqtt.client as mqtt

# inisiasi client mqtt
client = mqtt.Client(client_id="sub1", clean_session=False)

# Koneksikan ke broker
client.connect("127.0.0.1", port=1883)

# Subscribe ke salah satu topik
client.subscribe("/suhu/1", qos=1)

# Buat fungsi untuk menghandle message yang masuk
def on_message(client, obj, msg):
    print(msg.payload)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Daftarkan fungsi callback
client.on_connect = on_connect
client.on_message = on_message

try :
    # Buat infinite loop supaya subscriber tidak mati
    client.loop_forever()
except KeyboardInterrupt :
    print("Subscriber mati")