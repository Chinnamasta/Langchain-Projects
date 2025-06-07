from langchain.tools import tool
from email.message import EmailMessage
import smtplib
import ssl
import os

@tool
def envia_email(tool_input: str) -> str:
    """
    Envia um e-mail. Espera os dados no formato:
    destinatario=<email>; titulo=<titulo>; corpo=<mensagem>
    """
    email_usuario = os.getenv("EMAIL_USUARIO")
    senha_app = os.getenv("SENHA_APP")

    if not email_usuario or not senha_app:
        return "Erro: Credenciais de e-mail não configuradas."

    try:
        partes = dict(item.split("=", 1) for item in tool_input.split(";"))
        destinatario = partes["destinatario"].strip()
        titulo = partes["titulo"].strip()
        corpo = partes["corpo"].strip()
    except Exception as e:
        return f"Erro ao interpretar os dados: {e}"

    msg = EmailMessage()
    msg["From"] = email_usuario
    msg["To"] = destinatario
    msg["Subject"] = titulo
    msg.set_content(corpo)

    try:
        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as smtp:
            smtp.login(email_usuario, senha_app)
            smtp.send_message(msg)
        return "E-mail enviado com sucesso!"
    except Exception as e:
        return f"Erro ao enviar o e-mail: {e}"
