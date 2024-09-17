import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QColorDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QColor
import socket
import threading

# Создаем сокет

# Флаг для определения, когда программа должна быть переключена на веб-чат
is_web_chat = False

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.new_messages = []


    def initUI(self):
        self.setWindowTitle('Chat Client')
        self.setGeometry(100, 100, 400, 400)

        # Создание виджетов для ввода ника, IP-адреса и порта
        self.nick_label = QLabel('Nickname:')
        self.nick_input = QLineEdit()
        self.ip_label = QLabel('IP Address:')
        self.ip_input = QLineEdit()
        self.port_label = QLabel('Port:')
        self.port_input = QLineEdit()

        # Создание кнопки для подключения
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.connect_to_chat)

        # Создание текстового поля для отображения сообщений
        self.chat_window = QTextEdit()
        self.chat_window.setReadOnly(True)

        # Создание текстового поля для ввода сообщений
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)

        # Инициализируем цвет никнейма
        self.nick_color = QColor("red")

        # Компоновка виджетов
        layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.nick_label)
        input_layout.addWidget(self.nick_input)
        input_layout.addWidget(self.ip_label)
        input_layout.addWidget(self.ip_input)
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_input)
        input_layout.addWidget(self.connect_button)
        layout.addLayout(input_layout)
        layout.addWidget(self.chat_window)
        layout.addWidget(self.message_input)
        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_K:
            self.open_color_picker()
        else:
            super().keyPressEvent(event)

    def open_color_picker(self):
        # Открываем диалог выбора цвета
        color = QColorDialog.getColor(self.nick_color, self, "Цвет ника")
        if color.isValid():
            self.nick_color = color

    def send_message(self):
        message = self.message_input.text()
        nick_style = f"<span style='color:{self.nick_color.name()};'>{self.nick_input.text()}</span>"
        self.chat_window.append(f"{nick_style} : {message}")
        self.message_input.clear()
        self.worker.send_message(f"{nick_style} : {message}")

    def connect_to_chat(self):
        nick = f"<span style='color:{self.nick_color.name()};'>{self.nick_input.text()}</span>"
        host = self.ip_input.text()
        port = int(self.port_input.text())
        self.worker = WorkerSocket(host, port, nick, self.chat_window)
        self.worker.finished.connect(self.on_thread_finished)
        self.worker.start()
    def on_thread_finished(self, success):
        self.chat_window.clear()
        print(success)
        if success:
            self.chat_window.append(f"{self.worker.username} вы были подключены к чату ")
        else:
            self.chat_window.append("Неудачное подключение")
        # Блокируем ввод IP-адреса, порта и никнейма
        self.ip_input.setEnabled(False)
        self.port_input.setEnabled(False)
        self.nick_input.setEnabled(False)
        self.message_input.setEnabled(True)
        # Замена кнопки "Connect" на "Reconnect"
        self.connect_button.setText("Reconnect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.reconnectChat)
        
    def reconnectChat(self):
        # Разблокируем ввод IP-адреса, порта и никнейма
        self.ip_input.setEnabled(True)
        self.port_input.setEnabled(True)
        self.nick_input.setEnabled(True)
        self.message_input.setEnabled(False)
        # Замена кнопки "Reconnect" на "Connect"
        self.connect_button.setText("Connect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.connect_to_chat)


class WorkerSocket(QThread):
    finished = pyqtSignal(bool)
    userName = pyqtSignal(str)
    message = pyqtSignal(str)
    newMessage = pyqtSignal(str)

    def __init__(self, host, port, username, chat_window):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = None
        self.running = True
        self.chat_window = chat_window  # Сохраняем ссылку на chat_window

    def run(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.client_socket.send(self.username.encode('utf-8'))
            self.userName.emit(self.username)
            self.finished.emit(True)
            self.receive_messages()
        except Exception as e:
            self.finished.emit(False)
            print(f"Ошибка: {e}")

    def receive_messages(self):
        while self.running:
            try:
                data = self.client_socket.recv(4096)
                if data:
                    message = data.decode('utf-8')
                    self.chat_window.append(message)
            except:
                pass

    def send_message(self, message):
        if self.client_socket:
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.message.emit(message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения: {e}")

    def stop(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        self.quit()
        self.wait()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())
    # Включаем веб-чат

#Во первых, не видно текста, который отправляет другой клиент.
#На сервере сообщение удваивается при 2 подключённых клиентов. Узнать, происходит это из-за того, что оба клиента на 1 аёпи или же это проблема сервера