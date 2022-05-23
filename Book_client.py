import sys
import socket

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication

IP= "정해주세요"
Port = 2090

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP, Port))

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("log.ui", self)

        self.join_Btn.clicked.connect(self.join)
        self.pw_Edit.returnPressed.connect(self.try_login)
    def input(self):
        self.id_Edit=QLineEdit()
        self.pw_Edit=QLineEdit()
    
    def try_login(self):
        print("로그인시도")

    def join(self):
        sock.send("signup".encode())
        chat_window2 = reg()
        chat_window2.exec_()
        QCoreApplication.instance().quit

class reg(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("join.ui", self)

    def input(self):
        self.id_Edit=QLineEdit()
        self.pw_Edit=QLineEdit()
        self.repw_Edit=QLineEdit()
        self.name_Edit=QLineEdit()
        self.email_Edit=QLineEdit()
        self.emailnum_Edit=QLineEdit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_window = Login()
    chat_window.show()
    app.exec_()