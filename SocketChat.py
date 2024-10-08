import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import socket
import threading

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Флаг для определения, когда программа должна быть переключена на веб-чат
is_web_chat = False

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        # Используем self.nick_color для форматирования никнейма
        nick_style = f"<span style='color:{self.nick_color.name()};'>{self.nick_input.text()}</span>"
        message = [nick_style, self.message_input.text()]
        client_socket.send(str(message).encode('utf-8'))
        self.chat_window.append(f"{nick_style} :  {self.message_input.text()}")
        self.message_input.clear()
    def receiving_messages(self):
        while True:
            try:
                # Получаем сообщение от сервера
                message = list(client_socket.recv(4096).decode('utf-8'))
                self.chat_window.append(f"{message[0]} :  {message[1]}")
            except:
                # При ошибке закрываем соединение
                print("Произошла ошибка!")
                client_socket.close()
                break 
    def connect_to_chat(self):
        self.chat_window.clear()
        # Здесь должен быть код для переключения программы на веб-чат
        client_socket.connect((self.ip_input.text(), int(self.port_input.text())))
        self.chat_window.append('Вы подключены к чату')
        client_socket.send(self.nick_input.text().encode('utf-8'))

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
        client_socket.close()
        print("Сокет закрыт")
        # Код для переподключения к веб-чату
        self.chat_window.append('Переподключение к чату')

        # Разблокируем ввод IP-адреса, порта и никнейма
        self.ip_input.setEnabled(True)
        self.port_input.setEnabled(True)
        self.nick_input.setEnabled(True)
        self.message_input.setEnabled(False)

        # Замена кнопки "Reconnect" на "Connect"
        self.connect_button.setText("Connect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.connect_to_chat)

        # Добавьте код для переподключения к веб-чату
        # ...

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())
