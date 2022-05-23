import sys
import socket

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication

BUF_SIZE = 1024
IP= "10.10.20.37"
Port = 2090
a="3"
b="4"

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

        self.id_Btn.clicked.connect(self.chack_id)
        self.pw_Btn.clicked.connect(self.chack_pw)
        self.email_Btn.clicked.connect(self.chack_email)
        self.email_C_Btn.clicked.connect(self.chack_E_num)
    def chack_id(self):
        id=self.id_Edit.text()
        sock.send(id.encode())
        ck = sock.read(BUF_SIZE)
        if ck == "OK" :
            self.pw_Edit.setEnabled(True)
            self.repw_Edit.setEnabled(True)
            self.pw_Btn.setEnabled(True)
    def input(self):
        self.id_Edit=QLineEdit()
        self.id_Edit.setEnabled(False)
        #self.pw_Edit=QLineEdit()
        #self.repw_Edit=QLineEdit()
    def chack_pw(self):
        a=self.pw_Edit.text()
        b=self.repw_Edit.text()
        if a == b:
            self.name_Edit.setEnabled(True)
            self.email_Edit.setEnabled(True)
            self.email_Btn.setEnabled(True)
    def chack_email(self):
        #이메일 체크
        self.emailnum_Edit.setEnabled(True)
        self.email_C_Btn.setEnabled(True)
    def chack_E_num(self):

        self.join_Btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_window = Login()
    chat_window.show()
    app.exec_()