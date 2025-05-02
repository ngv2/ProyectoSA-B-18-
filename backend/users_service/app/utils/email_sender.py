import smtplib
from email.mime.text import MIMEText
import os


def send_confirmation_email(destinatario, token):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")

    link = f"http://localhost:5000/users/confirmation?token={token}"
    mensaje = MIMEText(f"Haz clic aquí para confirmar tu cuenta: {link}")
    mensaje["Subject"] = "Confirma tu cuenta"
    mensaje["From"] = email_from
    mensaje["To"] = destinatario

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(mensaje)
    except Exception as e:
        print("Error al enviar correo:", e)


def send_password_recovery_email(destinatario, token):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    email_from = os.getenv("EMAIL_FROM")

    link = f"http://localhost:5000/users/pass-recover?token={token}"
    mensaje = MIMEText(f"Haz clic aquí para restablecer tu contraseña: {link}")
    mensaje["Subject"] = "Recuperación de contraseña"
    mensaje["From"] = email_from
    mensaje["To"] = destinatario

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(mensaje)
    except Exception as e:
        print("Error al enviar correo:", e)
