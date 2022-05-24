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
        self.ui = uic.loadUi("Login.ui",self)

        self.join_Btn.clicked.connect(self.join)
        self.pw_Edit.returnPressed.connect(self.try_login)
    
    def try_login(self):
        print("로그인시도")

    def join(self):
        #sock.send("signup".encode())
        chat_window2 = reg()
        chat_window2.exec_()

class reg(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("register.ui", self)

        #버튼 이벤트들
        self.id_Btn.clicked.connect(self.chack_id)
        self.pw_Btn.clicked.connect(self.chack_pw)
        self.email_Btn.clicked.connect(self.chack_email)
        self.email_C_Btn.clicked.connect(self.chack_E_num)
        self.join_Btn.clicked.connect(self.join)

    def chack_id(self):
        id=self.id_Edit.text()
        sock.send(id.encode())
        ck = sock.read(BUF_SIZE)
        if ck == "!OK" :
            #아이디 중복확인이 완료했을시 입력칸 잠금해제
            self.pw_Edit.setEnabled(True)
            self.repw_Edit.setEnabled(True)
            self.pw_Btn.setEnabled(True)
    def chack_pw(self):
        a=self.pw_Edit.text()
        b=self.repw_Edit.text()
        if a == b:
            #비밀번호 확인이 완료했을시 입력칸 잠금해제
            self.name_Edit.setEnabled(True)
            self.email_Edit.setEnabled(True)
            self.email_Btn.setEnabled(True)
    def chack_email(self):
        #이메일 체크
        self.emailnum_Edit.setEnabled(True)
        self.email_C_Btn.setEnabled(True)
    def chack_E_num(self):
        self.join_Btn.setEnabled(True)
    def join(self):
        id=self.id_Edit.text()
        pw=self.pw_Edit.text()
        name=self.name_Edit.text()
        email=self.email_Edit.text()
        msg=id+"/"+pw+"/"+name+"/"+email
        #sock.send(msg.encode())
        print(msg)
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_window = Login()
    chat_window.show()
    app.exec_()