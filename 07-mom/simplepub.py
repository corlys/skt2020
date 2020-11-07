# import library paho mqtt
import paho.mqtt.client as mqtt

# Inisiasi mqtt client
client = mqtt.Client(client_id="pub1", clean_session=False)

# Buat koneksi ke broker
client.connect("127.0.0.1", port=1883)

# Publish message
client.publish("/suhu/1", payload="Hello 2", qos=1)