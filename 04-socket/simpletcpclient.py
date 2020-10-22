import socket

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kirim permintaan koneksi
sock.connect( ("127.0.0.1", 9999) )

# Kirim data
data = "Selamat sore"
sock.send( data.encode('ascii') )
# Terima balasan dari server
data = sock.recv(100)
data = data.decode('ascii')
print(data)