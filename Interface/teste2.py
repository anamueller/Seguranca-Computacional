import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from funcoes import *

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat Seguro')

        # Layout principal
        layout = QVBoxLayout()

        # Campo de mensagem a ser enviada
        self.message_input = QLineEdit()
        layout.addWidget(QLabel('Mensagem:'))
        layout.addWidget(self.message_input)

        # Opções de criptografia
        self.cipher_combo = QComboBox()
        self.cipher_combo.addItem('RC4')
        self.cipher_combo.addItem('S-DES')
        layout.addWidget(QLabel('Método de criptografia:'))
        layout.addWidget(self.cipher_combo)

        # Campo de chave
        self.key_input = QLineEdit()
        layout.addWidget(QLabel('Chave:'))
        layout.addWidget(self.key_input)

        # Campo de chave
        self.destino_input = QLineEdit()
        layout.addWidget(QLabel('IP de destino:'))
        layout.addWidget(self.destino_input)

        # Botão de enviar
        self.send_button = QPushButton('Enviar')
        self.send_button.clicked.connect(self.encrypt_message)
        layout.addWidget(self.send_button)

        # Campo de mensagem recebida
        self.received_message = QTextEdit()
        self.received_message.setReadOnly(True)
        layout.addWidget(QLabel('Mensagem recebida:'))
        layout.addWidget(self.received_message)

        self.setLayout(layout)
        self.show()

    def encrypt_message(self):
        message = self.message_input.text()
        cipher = self.cipher_combo.currentText()
        key = self.key_input.text()
        destiny =  self.destino_input.text()

        # Lógica de criptografia (RC4 ou S-DES)
        if cipher == 'RC4':
            encrypted_message = self.encrypt_rc4(message, key)
            self.enviar(key, destiny, encrypted_message)
        else:
            encrypted_message = self.encrypt_sdes(message, key)
            self.enviar(key, destiny, encrypted_message)

        receive = self.receber()

        self.received_message.setText(receive)
        
    def receber(self):
        return 'teste'
    
    def encrypt_rc4(self, message, key):
        # Implementação do algoritmo de criptografia RC4
        return 'ana'

    def encrypt_sdes(self, message, key):
        # Implementação do algoritmo de criptografia S-DES
        return 'ana'
    
    def enviar(self, key, destino, message):
        #envia mensagem ao ip de destino com as informações da chave, e algoritmo usado
        print(key)
        print(destino)
        return 0
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptoApp()
    sys.exit(app.exec_())
