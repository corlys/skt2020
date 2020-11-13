import zerorpc
import threading
# import library paho mqtt
import paho.mqtt.client as mqtt
import time

nik = input("NIK : ")
nama = input("Nama : ")
alamat = input("Alamat : ")
penyakit = input("Penyakit : ")

server_ip = input("IP RPC Server Rumah Sakit : ")
server_port = input("Port RPC Server Rumah Sakit : ")

c = zerorpc.Client()
c.connect("tcp://"+server_ip+":"+server_port)

c.sendData(nik, nama, alamat, penyakit)   

while True:
    print(c.getData(nik))
    # time.sleep(20)