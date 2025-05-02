import smtplib
from email.mime.text import MIMEText
import os

def enviar_resumen_compra(destinatario, resumen):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")

    mensaje = MIMEText(resumen, "html")
    mensaje["Subject"] = "Resumen de tu compra"
    mensaje["From"] = email_from
    mensaje["To"] = destinatario

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(mensaje)
    except Exception as e:
        print("Error al enviar correo:", e)
