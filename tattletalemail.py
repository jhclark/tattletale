import smtplib
from email.mime.text import MIMEText

def sendMail(config: configparser.ConfigParser, fro: str, to: str, subject: str, body: str):
    emailAddress = config.get('email', 'emailAddress')
    emailPassword = config.get('email', 'emailPassword')
    
    msg = MIMEText(body)

    msg['Subject'] = subject
    msg['From'] = fro
    msg['To'] = to

    # send message using gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(emailAddress, emailPassword)
    server.sendmail(fro, [to], msg.as_string())
    server.quit()

#sendMail(emailAddress, emailAddress, "hello", "test email")