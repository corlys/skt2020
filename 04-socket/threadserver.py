# Import socket
import socket
import threading

# Inisiasi socket TCP/IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind
sock.bind( ("0.0.0.0", 9999) )

# Listen sebanyak jumlah backlog
sock.listen(10)

# Fungsi yang akan dieksekusi pada setiap thread
def handle_thread(conn):
    try :
        while True :
            # Receive data dari client
            data = conn.recv(100)
            data = data.decode('ascii')
            data = "OK "+data
            # Kirim balik ke client
            conn.send(data.encode('ascii'))
    except (socket.error, KeyboardInterrupt):
        conn.close()
        print("Client menutup koneksi")

try :
    while True :
        # Terima permintaan koneksi
        conn, client_addr = sock.accept()
        # Buat thread baru setiap ada permintaan koneksi dari client
        clientThread = threading.Thread(target=handle_thread, args=(conn,))
        clientThread.start()
except KeyboardInterrupt :
    print("Server mati")
    
    
