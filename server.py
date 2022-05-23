from ast import Continue
from asyncio.windows_events import NULL
import socket
import threading
import sqlite3

PORT = 2090
BUF_SIZE = 1024
lock = threading.Lock()
clnt_imfor = []
clnt_cnt = 0

con = sqlite3.connect('Book.db')

c = con.cursor()

def handle_clnt(clnt_sock):
    for i in range(0, clnt_cnt):
        if clnt_imfor[i][1] == clnt_sock:
            clnt_num = i
            break

        while True:
            clnt_msg = clnt_sock.recv(BUF_SIZE)

            if not clnt_msg:
                lock.acquire()
                delete_imfor(clnt_sock)
                lock.release()
                break

            clnt_msg = clnt_msg.encode()

            if 'signup' in clnt_msg:
                sign_up(clnt_sock)


def sign_up(clnt_sock):
    check = 0
    user_data = []
    while True:
        imfor = clnt_sock.recv(BUF_SIZE)
        imfor = imfor.decode("UTF–8")

        c.execute("SELECT id FROM Users")
        for row in c.fetchall():
            if row == imfor:
                clnt_sock.send('NO'.encode())
                check = 1
                break
        if check == 1:
            continue
        clnt_sock.send('OK'.encode())
        user_data.append(imfor)
        print(user_data)
        imfor = clnt_sock.recv(BUF_SIZE) # password/name/email
        imfor = imfor.split('/')  # 구분자 /로 잘라서 리스트 생성
        imfor[0] = imfor[0].decode("UTF–8")    # imfor[0]은 password라서 디코딩
        user_data.append(imfor)       # user_data 리스트에 추가
        print(user_data)
        query = "INSERT INTO Users(id, password, name, email) VALUES(?, ?, ?, ?)" 
        c.executemany(query, user_data) # DB에 user_data 추가
        con.commit()



def login(clnt_sock):
    while True:
        imfor = clnt_sock.recv(BUF_SIZE)  # id/password
        imfor = imfor.split('/')          
        for i in range(2):         
            imfor[i] = imfor[i].decode("UTF–8")   
        user_id = imfor[0]     
        c.execute("SELECT password FROM Users where id=?", user_id) # DB에서 id 같은 password 컬럼 선택
        user_pw = c.fetchone()             # 한 행 추출

        '''없는 id이면 null?
        if user_pw == NULL:
            continue'''
     
        if imfor[1] == user_pw:
            #로그인성공 시그널
            #clnt_sock.send('OK'.encode())    
            print("login sucess")
            break
        else:
            #로그인실패 시그널
            #clnt_sock.send('NO'.encode())    
            print("login failure")
            continue
        
def find_id(clnt_sock):
    imfor = clnt_sock.recv(BUF_SIZE) # name/email
    imfor = imfor.split('/')
    user_name = imfor[0]
    c.execute("SELECT id, email FROM Users where name=?", user_name)
    row = c.fetchone()
    user_id = row[0]
    user_email = row[1]
    if imfor[1] == user_email:
        #id 보내기(메일로?)
        #clnt_sock.send(user_id.encode()) 
    else:
        #정보일치x


def find_pw(clnt_sock):
    imfor = clnt_sock.recv(BUF_SIZE) #id/name/email
    imfor = imfor.split('/')
    user_id = imfor[0]
    c.execute("SELECT password, name, email FROM Users where id=?", user_id)
    row = c.fetchone()
    user_name = imfor[1]
    user_email = imfor[2]
    if imfor[1] == user_name:
        if imfor[2] == user_email:
            #password 보내기
            #clnt_sock.send(user_email.encode())
        else:
            #정보일치x
    else:
        #정보일치x




def delete_imfor(clnt_sock):
    global clnt_cnt
    for i in range(0, clnt_cnt):
        if clnt_sock == clnt_imfor[i][1]:
            print("%s님께서 접속 종료하셨습니다." %clnt_imfor[i][0])
            while i < clnt_cnt - 1:
                # clnt_imfor[i][0] = clnt_imfor[i + 1][0]
                # clnt_imfor[i][1] = clnt_imfor[i + 1][1]
                # clnt_imfor[i][2] = clnt_imfor[i + 1][2]
                i += 1
            break
    clnt_cnt -= 1

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', PORT))
    sock.listen(5)

    while True:
        clnt_sock, addr = sock.accept()

        lock.acquire()

        clnt_imfor.insert(clnt_cnt, [clnt_sock])
        clnt_cnt += 1

        lock.release()

        t = threading.Thread(target=handle_clnt, args=(clnt_sock,))
        t.start()