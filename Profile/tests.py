import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()



password = "diodpasswordis12345"
from_user = "SocialNetworkdiod@gmail.com"
to_user = "danilaprig@gmail.com"
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(from_user, password)
"""# add in the message body
msg.attach(MIMEText(message, 'plain'))"""

token = random.randint(100000, 999999)

msg['Subject'] = "Подтверждение почты"

msg.attach(MIMEText(f"Ваш код подтверждения: {str(token)}", 'plain'))

server.sendmail(from_user, to_user, msg.as_string())

server.quit()