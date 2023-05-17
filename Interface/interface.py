import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from funcoes import *


app = QApplication([])
window = QWidget()
layout = QVBoxLayout()


enviar = QPushButton('Enviar')
recebido = QLineEdit('teste')
recebido.setAlignment(Qt.AlignCenter)
recebido.setReadOnly(True)

mensagem = QLineEdit()
endereco_IP = QLineEdit()
chave = QLineEdit()



layout.addWidget(QLabel('Digite sua mensagem abaixo'))
layout.addWidget(mensagem)
layout.addWidget(QLabel('Escolha seu método de criptografia'))
layout.addWidget(QRadioButton('RC4'))
layout.addWidget(QRadioButton('S-DES'))
layout.addWidget(QLabel('Digite a chave'))
layout.addWidget(chave)
layout.addWidget(QLabel('Digite o IP'))
layout.addWidget(endereco_IP)
layout.addWidget(enviar)
layout.addWidget(QLabel('Mensagem recebida'))
layout.addWidget(recebido)

window.setLayout(layout)
window.show()

enviar.clicked.connect(on_button_clicked())

app.exec()

