from PyQt5.QtWidgets import *

def on_button_clicked():
    alert = QMessageBox()
    alert.setText('Mensagem Enviada')
    alert.exec()
