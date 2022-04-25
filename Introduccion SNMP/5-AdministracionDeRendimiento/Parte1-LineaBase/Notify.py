import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMA_SPACE = ", "
# Define params
RRD_PATH = "RRD/"
IMG_PATH = "IMG/"
RRD_FILE = "trend.rrd"

MAIL_SENDER = "dummycuenta3@gmail.com"
MAIL_RECV_IP = "dummycuenta3@gmail.com"
MAIL_SERVER = "smtp.gmail.com:587"
PASSWORD = "Secreto123"

def sendAlertAttached( subject: str ) -> None:
    # Envia un correo electronico adjuntando la imagenn en IMG
    email_msg = MIMEMultipart()
    email_msg["Subject"] = subject
    email_msg["From"] = MAIL_SENDER
    email_msg["To"] = MAIL_RECV_IP
    with open(IMG_PATH + "detection.png", "rb") as fp:
        img = MIMEImage(fp.read())
    email_msg.attach(img)
    s = smtplib.SMTP(MAIL_SERVER)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(MAIL_SENDER, PASSWORD)
    s.sendmail(MAIL_SENDER, MAIL_RECV_IP, email_msg.as_string())
    s.quit()
