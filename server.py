import socket
import threading

# Список подключенных клиентов
clients = []

def broadcast(message, sender_conn):
    for conn in clients:
        if conn != sender_conn:
            try:
                conn.send(message)
                print(message)
            except:
                print("Неудача")
                conn.close()
                clients.remove(conn)

def handle(conn):
    while True:
        try:
            message = conn.recv(4096)
            text = message.decode().split(" ")
            print(message.decode())
            if text[1] == 'EXIT':
                print("ВЫХОООД")
                index = clients.index(conn)
                clients.remove(conn)
                conn.close()
                print(f'Клиент {index} отключился')
                break
            broadcast(message, conn)
        except:
            index = clients.index(conn)
            clients.remove(conn)
            conn.close()
            print(f'Клиент {index} отключился')
            break

def receive():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.0.152', 9090))
    server_socket.listen(100)
    print('Сервер запущен и слушает...')

    while True:
        conn, addr = server_socket.accept()
        print(f'Подключение от {str(addr)}')

        clients.append(conn)
        nick = conn.recv(1024).decode('utf-8')
        conn.send(nick.encode('utf-8'))
        print(f'Новый клиент с ником {nick}')
        broadcast(f'{nick} подключился к чату!'.encode('utf-8'), conn)
        conn.send('Вы теперь подключены к чату!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(conn,))
        thread.start()

print('Сервер запускается...')
receive()
