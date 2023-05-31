#Leonardo Silva Pinto e Ana Clara Mueller Miranda
#formato de execução do código:
#python3 interface.py porta_destino porta_local
#exemplo interface.py 3000 3000

import sys
import typing
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from queue import Queue
import subprocess
import socket
from PyQt5.QtCore import QObject, Qt, QThread, pyqtSignal

IP_LOCAL = '0.0.0.0'
PORTA_LOCAL = 8005
PORTA_DEST = 8004
DEBUG = True

class ServidorThread(QThread):
    new_message = pyqtSignal(str)
    encrypted_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        host = IP_LOCAL 
        porta = PORTA_LOCAL
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket.bind((host, porta))
        servidor_socket.listen(1)

        conexao, endereco = servidor_socket.accept()
        self.new_message.emit(f"Conectado com: {endereco}")

        while True:
            mensagem = conexao.recv(1024).decode()
            if not mensagem:
                break
            self.encrypted_received.emit(mensagem)

        conexao.close()
        servidor_socket.close()


class ClientThread(QThread):
    enviar_mensagem = pyqtSignal(str)
    new_message = pyqtSignal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.message_queue = Queue()

    def run(self):
        # Configure o socket do cliente
        host = self.ip # Insira o IP do servidor
        porta = PORTA_DEST
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client_socket.connect((host, porta))
            self.new_message.emit("Conexão com o servidor")

            while True:
                # Verifique se há uma nova mensagem na fila
                if not self.message_queue.empty():
                    mensagem = self.message_queue.get()

                    client_socket.send(mensagem.encode())

        except ConnectionRefusedError:
            self.new_message.emit("Não foi possível conectar ao servidor.\nTente se conectar novamente.")

        finally:
            client_socket.close()


    def enviar(self, mensagem):
        self.message_queue.put(mensagem)


class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.key = ''
        self.cipher = ''
        
        # Criar servidor
        self.servidor_thread = ServidorThread()
        self.servidor_thread.new_message.connect(self.update)
        self.servidor_thread.encrypted_received.connect(self.decrypt)
        self.servidor_thread.start()

    def update(self, text):
        self.received_message.append(text)

    def decrypt(self, text):
        if DEBUG:
            print("Mensagem recebida: ",text)
        if self.cipher == 'RC4':
            subprocess.run(['gcc', '-o', 'test', 'rca.c']) # compile
            result = subprocess.run(['./test', "O", text, self.key], stdout=subprocess.PIPE) # run
            output = result.stdout.decode("utf-8") # get output
            self.update("< " + output)
            if DEBUG:
                print("Mensagem descriptografada rc4: ",output)
        elif self.cipher == 'S-DES':
            subprocess.run(['gcc', '-o', 'test', 'des.c']) # compile
            result = subprocess.run(['./test', "O",text, self.key], stdout=subprocess.PIPE) # run
            output = result.stdout.decode("utf-8") # get output
            self.update("< " + output)
            if DEBUG:
                print("Mensagem descriptografada sdes: ",output)
            
        

    def initUI(self):
        self.setWindowTitle('Chat Seguro')

        # Layout principal
        layout = QVBoxLayout()

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

        # Botão de conectar
        self.conn_button = QPushButton('Connect')
        layout.addWidget(self.conn_button)
        self.conn_button.clicked.connect(self.connect)

        # Botão de conectar
        self.refresh_button = QPushButton('Refresh Cypher')
        layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_cypher)

        # Campo de mensagem a ser enviada
        self.message_input = QLineEdit()
        layout.addWidget(QLabel('Mensagem:'))
        layout.addWidget(self.message_input)

        # Botão de enviar
        self.send_button = QPushButton('Enviar')
        layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.encrypt_message)

        # Campo de mensagem recebida
        self.received_message = QTextEdit()
        self.received_message.setReadOnly(True)
        layout.addWidget(QLabel('Mensagem recebida:'))
        layout.addWidget(self.received_message)

        self.receive = ''
        self.setLayout(layout)
        self.show()

    def connect(self):
        destiny =  self.destino_input.text()
        self.client_thread = ClientThread(destiny)
        self.client_thread.new_message.connect(self.update)
        self.client_thread.start()

        self.refresh_cypher()

    def refresh_cypher(self):
        cipher = self.cipher_combo.currentText()
        self.cipher = cipher

        key = self.key_input.text()
        self.key = key


    def encrypt_message(self):
        message = self.message_input.text()
        if message == "":
            return
        self.update("> " + message)
        cipher = self.cipher_combo.currentText()
        key = self.key_input.text()
        destiny =  self.destino_input.text()
        
        if DEBUG:
            print("Mensagem enviada: ",message)
        
        # Lógica de criptografia (RC4 ou S-DES)
        if cipher == 'RC4':
            encrypted_message = self.encrypt_rc4(message, key)
            self.enviar(key, destiny, encrypted_message)
        else:
            encrypted_message = self.encrypt_sdes(message, key)
            self.enviar(key, destiny, encrypted_message)

        #self.client_thread.nova_mensagem.emit(message)
        # self.received_message.append(message)
        self.message_input.clear()
            
    def encrypt_rc4(self, message, key):
        # Implementação do algoritmo de criptografia RC4
        subprocess.run(['gcc', '-o', 'test', 'rca.c']) # compile
        result = subprocess.run(['./test', "C", message, key], stdout=subprocess.PIPE) # run
        output = result.stdout.decode() # get output
        if DEBUG:
            print("Mensagem criptografada rc4: ",output)
        return output #retornando a mensagem criptografada

    def encrypt_sdes(self, message, key):
        # Implementação do algoritmo de criptografia S-DES
        subprocess.run(['gcc', '-o', 'test', 'des.c']) # compile
        result = subprocess.run(['./test', "C",message, key], stdout=subprocess.PIPE) # run
        output = result.stdout.decode("utf-8") # get output
        if DEBUG:
            print("Mensagem criptografada sdes: ",output)
        
        return output #retornando a mensagem criptografada
    
    def enviar(self, key, destino, message):
        #envia mensagem ao ip de destino com as informações da chave, e algoritmo usado
        self.client_thread.enviar(message)
        return 0
    

if __name__ == '__main__':
    PORTA_DEST = int(sys.argv[1])
    PORTA_LOCAL = int(sys.argv[2])
    app = QApplication(sys.argv)
    window = CryptoApp()
    sys.exit(app.exec_())
