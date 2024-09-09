import socket
import threading

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('192.168.1.107', 9090))

# Получаем никнейм от пользователя
nickname = input("Введите ваш никнейм: ")
client_socket.send(nickname.encode('utf-8'))

def receive():
    while True:
        try:
            # Получаем сообщение от сервера
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # При ошибке закрываем соединение
            print("Произошла ошибка!")
            client_socket.close()
            break

def write():
    while True:
        try:
            # Отправляем сообщение на сервер
            TEXT = input("")
            # if len(TEXT)>=5:
            message = f'{nickname}: {TEXT}'
            client_socket.send(message.encode('utf-8'))
        except:
            # При ошибке закрываем соединение
            print("Произошла ошибка!")
            client_socket.close()
            break

# Запускаем два потока: для приема и отправки сообщений
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
