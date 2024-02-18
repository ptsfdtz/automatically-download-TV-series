import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, recipient_email, subject, body):
    if "@qq.com" in sender_email:
        smtp_server = "smtp.qq.com"
        smtp_port = 587
    elif "@gmail.com" in sender_email:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    else:
        print("不支持的邮箱地址")
        return

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        server.starttls()

        server.login(sender_email, sender_password)

        server.sendmail(sender_email, recipient_email, message.as_string())

    print("邮件已发送成功！")

sender_email = "@gmail.com"
sender_password = ""
recipient_email = "@qq.com"
subject = "head"
body = "test"

send_email(sender_email, sender_password, recipient_email, subject, body)
