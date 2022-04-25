import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# Constantes
COMA_SPACE = ", "
MAIL_FROM = "pruebasc121@gmail.com" # Direccion de correo de uso
MAIL_TO = "nacxit.developer@gmail.com" # Direccion correo destino
MAIL_SENDER = "smtp.gmail.com:587"
PASSWORD = "passwordPerron"


def sendAlertAttached( subject: str, image_path: str ) -> None:
    # Envia un correo electronico adjuntando la imagenn en IMG
    email_message = MIMEMultipart()
    email_message["Subject"] = subject
    email_message["From"] = MAIL_SENDER
    email_message["To"] = MAIL_TO
    with open(image_path) as file_image:
        image = MIMEImage(file_image.read())
    email_message.attach(image)
    s = smtplib.SMTP(MAIL_FROM)
    s.starttls()
    # Login Credentials for sending the email
    s.login(MAIL_FROM, PASSWORD)
    s.sendmail(MAIL_FROM, MAIL_TO, email_message.as_string())
    s.quit()
    print(f"Correo enviado correctamente a {MAIL_TO}")