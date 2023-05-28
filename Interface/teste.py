import sys
import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from funcoes import *

info = []
received = 'test ahahdhbasfhsldfsdhbfjhadbjkgh\nbjghbarjkhgbarlkgliaeqygh'

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Seguro")
        
        self.mensagem = QLineEdit('', self)
        self.chave = QLineEdit('', self)
        self.endereco_IP = QLineEdit('', self)
        self.recebido = QLineEdit(received, self)
        self.recebido.resize(500,400)
        enviar = QPushButton('Enviar')

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Digite sua mensagem abaixo'))
        layout.addWidget(self.mensagem)
        layout.addWidget(QLabel('Escolha seu método de criptografia'))
        layout.addWidget(QRadioButton('RC4'))
        layout.addWidget(QRadioButton('S-DES'))
        layout.addWidget(QLabel('Digite a chave'))
        layout.addWidget(self.chave)
        layout.addWidget(QLabel('Digite o IP'))
        layout.addWidget(self.endereco_IP)
        layout.addWidget(enviar)
        layout.addWidget(QLabel('Mensagem recebida'))
        layout.addWidget(self.recebido)


        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        enviar.clicked.connect(lambda: do_action())
        def do_action():
            info.clear()
            # getting text from the line edit
            info.append(self.mensagem.text())
            info.append(self.chave.text())
            info.append(self.endereco_IP.text())
            print(info)
        
        
        


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
