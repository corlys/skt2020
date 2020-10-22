# Import socket
import socket

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind
sock.bind( ("0.0.0.0", 9999) )

# Listen sebanyak jumlah backlog
sock.listen(10)

while True :
    # Terima permintaan koneksi
    conn, client_addr = sock.accept()
    # Receive data dari client
    data = conn.recv(100)
    data = data.decode('ascii')
    data = "OK "+data
    # Kirim balik ke client
    conn.send(data.encode('ascii'))
    # Tutup koneksi (opsional)
    # conn.close()
