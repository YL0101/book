import smtplib
from email.mime.text import MIMEText # 이메일 전송을 위한 라이브러리 import

ses = smtplib.SMTP('smtp.gmail.com', 587) # smtp 세션 설정
ses.starttls()

ses.login('saverock1235@gmail.com', "ohjo tynp pojs xjcx") # 이메일을 보낼 gmail 계정에 접속

msg = MIMEText('보낼 메세지 내용') # 보낼 메세지 내용을 적는다
msg['subject'] = '이메일의 제목' # 보낼 이메일의 제목을 적는다

ses.sendmail("saverock1235@gmail.com", "이메일을 받을 계정", msg.as_string()) # 앞에는 위에서 설정한 계정, 두번째에는 이메일을 보낼 계정을 입력

ses.quit() # 세선종료
