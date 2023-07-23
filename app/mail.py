'''
メール関連の処理を定義します。具体的には、
メール生成と送信の機能を実装します。
'''
import win32com.client
import pythoncom

class mail_template:
    def __init__(self, to, subject, body):
        pythoncom.CoInitialize()  
        self.outlook = win32com.client.Dispatch("Outlook.Application")
        self.mail = self.outlook.CreateItem(0)
        self.mail.to = to
        self.mail.subject = subject
        self.body = body
        self.rn = '***'  # ラジオ名と区別するためにrnとしてる、入力は任意
        self.address = '〒***-****\n香川県高松市****\n氏名:****'  # addressは住所の方

    # the rest of your code...


    def send_email(self):

        self.mail.bodyFormat = 1  
        self.mail.body = f'''RN : {self.rn}\n\n{self.body}\n\n{self.address}'''
        self.mail.display(True)
