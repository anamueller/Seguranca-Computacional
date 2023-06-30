import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import randint
from queue import Queue
import subprocess
import socket
from PyQt5.QtCore import QThread, pyqtSignal

IP_LOCAL = '0.0.0.0'
PORTA_LOCAL = 3000
PORTA_DEST = 3000
DEBUG = True
PRIME = 17
BASE = 5

class ServidorThread(QThread):
    new_message = pyqtSignal(str)
    encrypted_received = pyqtSignal(str)
    server_key = pyqtSignal(str)

    def __init__(self):
        self.dh_set = False
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

            if not self.dh_set:
                self.server_key.emit(mensagem)
                print("CHAVE PUBLICA SERVIDOR: ", mensagem)
                self.dh_set = True
            else:
                self.encrypted_received.emit(mensagem)

        conexao.close()
        servidor_socket.close()


class ClientThread(QThread):
    enviar_mensagem = pyqtSignal(str)
    new_message = pyqtSignal(str)

    def __init__(self, ip):
        super().__init__()
        self.ip = '127.0.0.1'
        #self.ip = ip
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
        self.DH = False
        self.dh_set = False
        self.server_public_key = None
        self.client_private_key = None
        
        # Criar servidor
        self.servidor_thread = ServidorThread()
        self.servidor_thread.new_message.connect(self.update)
        self.servidor_thread.encrypted_received.connect(self.decrypt)
        self.servidor_thread.server_key.connect(self.shared_key)
        self.servidor_thread.start()

    def trocaDH(self):
        if self.dh_check.isChecked() == True:
            self.DH = True
        else:
            self.DH = False

    def update(self, text):
        self.received_message.append(text)

    def decrypt(self, text):
        if DEBUG:
            print("Mensagem recebida: ",text)
        if self.cipher == 'RC4':
            if self.DH:
                print("chave compartilhada: ", self.s_key)
                self.key = self.key + str(self.s_key)
            subprocess.run(['gcc', '-o', 'test', 'rca.c']) # compile
            result = subprocess.run(['./test', "O", text, self.key], stdout=subprocess.PIPE) # run
            output = result.stdout.decode("utf-8") # get output
            self.update("< " + output)
            if DEBUG:
                print("Mensagem descriptografada rc4: ",output)
        elif self.cipher == 'S-DES':
            if self.DH:
                print("chave compartilhada: ", self.s_key)
                self.key = self.key + str(self.s_key)
            decrypted_message = ''
            for i in range(0, len(text),8):
                subprocess.run(['gcc', '-o', 'test', 'des.c']) # compile
                result = subprocess.run(['./test', "O",text[i:i+8], self.key], stdout=subprocess.PIPE) # run
                output = result.stdout.decode("utf-8") # get output
                decrypted_message = decrypted_message + chr(int(output, 2))
            print(decrypted_message)
            self.update("< " + decrypted_message)
            if DEBUG:
                print("Mensagem descriptografada sdes: ",output)
        elif self.cipher == 'ECB':
            decrypted_message = ''
            j=0
            for i in range(0,len(text),8):
                print('ECB cifragem com caracter', j)
                j=j+1
                stringbits = text[i:i+8]

                print("caracter em formato de 8 bits:",stringbits)

                subprocess.run(['gcc', '-o', 'test', 'des.c']) # compile
                result = subprocess.run(['./test', "O",stringbits, self.key], stdout=subprocess.PIPE) # run
                output = result.stdout.decode("utf-8") # get output
                print(output)
                decrypted_message = decrypted_message + chr(int(output, 2))
            self.update("< " + decrypted_message)
            if DEBUG:
                print("Mensagem descriptografada sdes: ",decrypted_message)
        elif self.cipher == 'CBC':
            pass

    def initUI(self):
        self.setWindowTitle('Chat Seguro')

        # Layout principal
        layout = QVBoxLayout()

        # Campo de chave
        self.destino_input = QLineEdit()
        layout.addWidget(QLabel('IP de destino:'))
        layout.addWidget(self.destino_input)

        # Botão de conectar
        self.conn_button = QPushButton('Connect')
        layout.addWidget(self.conn_button)
        self.conn_button.clicked.connect(self.connect)

        # Opções de criptografia
        self.cipher_combo = QComboBox()
        self.cipher_combo.addItem('RC4')
        self.cipher_combo.addItem('S-DES')
        self.cipher_combo.addItem('ECB')
        self.cipher_combo.addItem('CBC')
        layout.addWidget(QLabel('Método de criptografia:'))
        layout.addWidget(self.cipher_combo)

        # Opcao DH
        self.dh_check = QCheckBox("Troca de chaves DH", self)
        self.dh_check.stateChanged.connect(self.trocaDH)
        layout.addWidget(self.dh_check)

        # Campo de chave
        self.key_input = QLineEdit()
        layout.addWidget(QLabel('Chave:'))
        layout.addWidget(self.key_input)

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

    def refresh_cypher(self):
        cipher = self.cipher_combo.currentText()
        self.cipher = cipher
        if not self.dh_set:
            self.make_key()
            self.dh_set = True
        key = self.key_input.text()
        self.key = key
        print("CIFRAS ATUALIZADAS")


    def encrypt_message(self):
        message = self.message_input.text()
        if message == "":
            return
        self.update("> " + message)
        
        if DEBUG:
            print("Mensagem enviada: ",message)
        
        # Lógica de criptografia (RC4 ou S-DES)
        if self.cipher == 'RC4':
            if self.DH:
                print("chave compartilhada: ", self.s_key)
                self.key = self.key + str(self.s_key)
            encrypted_message = self.encrypt_rc4(message, self.key)
            self.enviar(self.key, encrypted_message)
        elif self.cipher == 'S-DES':
            if self.DH:
                print("chave compartilhada: ", self.s_key)
                self.key = self.key + str(self.s_key)
            encrypted_message = ''
           
            #transformando em uma string de 8 bit
            bitcaracter = map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message]))
            stringbits = ''.join(str(e) for e in bitcaracter)
            print("string em formato de 8 bits:",stringbits)

            for i in range(0,len(stringbits),8):
                #encriptando os 8 bits e transformando em um char novamente para adicionar
                encrypted_message = encrypted_message + self.encrypt_sdes(stringbits[i:i+8], self.key)
            
            print(":::", encrypted_message)
            self.enviar(self.key, encrypted_message)
        elif self.cipher == 'ECB':
            encrypted_message = ''
            for i in range(len(message)):
                print('ECB cifragem com caracter', i+1)
                string = message[i]

                #transformando caracter em uma string de 8 bit
                bitcaracter = ' '.join(format(i, '08b') for i in bytearray(string, encoding = 'utf-8')).split()
                stringbits = bitcaracter[0]
                print("caracter em formato de 8 bits:",stringbits)

                #encriptando os 8 bits e transformando em um char novamente para adicionar
                encrypted_message = encrypted_message + self.encrypt_sdes(stringbits, self.key)
            print(":::", encrypted_message)
            self.enviar(self.key, encrypted_message)
        elif self.cipher == 'CBC':
            encrypted_message = ''
            for i in range(8):
                print('CBC cifragem com caracter ', i+1)
                string = message[i]

                if i==0: #primeiro xor com vetor de inicialização
                    invector = randint(0,9) #vetor de inicialização
                    bitxorado = invector ^ int(string)

                    #transformando caracter em uma string de 8 bit
                    bitcaracter = ' '.join(format(i, '08b') for i in bytearray(chr(bitxorado), encoding = 'utf-8')).split()
                    stringbits = bitcaracter[0]
                    print("caracter em formato de 8 bits:",stringbits)

                    #encriptando os 8 bits e transformando em um char novamente para adicionar
                    encrypted_message = encrypted_message + self.encrypt_sdes(stringbits, self.key)
                
                if i>=1:  #proximo usam a mensagem anterior para xorar
                    bitxorado = ord(encrypted_message[i-1]) ^ int(string)

                    #transformando caracter em uma string de 8 bit
                    bitcaracter = ' '.join(format(i, '08b') for i in bytearray(chr(bitxorado), encoding = 'utf-8')).split()
                    stringbits = bitcaracter[0]
                    print("caracter em formato de 8 bits:",stringbits)

                    #encriptando os 8 bits e transformando em um char novamente para adicionar
                    encrypted_message = encrypted_message + self.encrypt_sdes(stringbits, self.key)
            self.enviar(self.key, encrypted_message)
            
        self.message_input.clear()

    def make_key(self):
        self.client_private_key = randint(2,PRIME)
        client_public_key = str(pow(BASE,self.client_private_key,PRIME))
        self.client_thread.enviar(client_public_key)
        print("CHAVE PRIVADA CLIENTE: ", self.client_private_key)
        print("CHAVE PUBLICA CLIENTE: ", client_public_key)

        if not (self.server_public_key is None or self.client_private_key is None):
            self.s_key = pow(PRIME, int(self.server_public_key), self.client_private_key)
            #print(self.s_key)

    def shared_key(self, text):
        self.server_public_key = text

        if not (self.server_public_key is None or self.client_private_key is None):
            self.s_key = pow(PRIME, int(self.server_public_key), self.client_private_key)
            #print(self.s_key)

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
    
    def enviar(self, key, message):
        #envia mensagem ao ip de destino com as informações da chave, e algoritmo usado
        self.client_thread.enviar(message)
        return 0
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        PORTA_DEST = int(sys.argv[1])
        PORTA_LOCAL = int(sys.argv[2])
    app = QApplication(sys.argv)
    window = CryptoApp()
    sys.exit(app.exec_())