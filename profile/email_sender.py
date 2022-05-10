import random

from django.core.mail import EmailMultiAlternatives

def send_submit_email(to_user):

    token = random.randint(100000, 999999)

    subj = "diod    ^`^t email verification"
    text = f"hi! you received this email because you tried to register on diod.cf. if you didn't, skip this email. your authentification code is: <strong>{str(token)}"
    html = f"<table style='padding:20px;background:#34373C;color:white;font-size:24px;font-family:Bahnschrift;text-align:center;'><tr><td>hi! you received this email because you tried to register on <a href='https://diod.cf'>diod.cf</a></td></tr><tr><td style='font-size:14px;font-style:italic;color:#888888'>if you didn't, skip this email<br></td></tr><tr><td style='font-size:18px'>your authentification code is: <strong>{str(token)}</strong></td></tr></table>"

    msg = EmailMultiAlternatives(subj, text, "auth@diod.cf", [to_user])
    msg.attach_alternative(html, "text/html")
    msg.send()

    return token
