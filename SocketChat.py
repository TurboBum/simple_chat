import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QThread, pyqtSignal

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

    def connect_to_chat(self):
        # Здесь должен быть код для переключения программы на веб-чат
        self.chat_window.append('Switching to web chat...')

        # Блокируем ввод IP-адреса, порта и никнейма
        self.ip_input.setEnabled(False)
        self.port_input.setEnabled(False)
        self.nick_input.setEnabled(False)
        self.message_input.setEnabled(True)

        # Добавьте код для создания веб-чата
        # ...

        # Замена кнопки "Connect" на "Reconnect"
        self.connect_button.setText("Reconnect")
        self.connect_button.clicked.disconnect()
        self.connect_button.clicked.connect(self.reconnectChat)

    def reconnectChat(self):
        # Код для переподключения к веб-чату
        self.chat_window.append('Reconnecting to web chat...')

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



    def send_message(self):
        # Здесь должен быть код для отправки сообщения в чат
        message = self.message_input.text()
        self.chat_window.append(f'{self.nick_input.text()}: {message}')
        self.message_input.clear()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())
