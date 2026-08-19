import os
from dotenv import load_dotenv
from pydantic import SecretStr
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType, NameEmail

load_dotenv()

senha_app = SecretStr(os.getenv("MAIL_PASSWORD", ""))

config = ConnectionConfig(MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
                          MAIL_PASSWORD=senha_app,
                          MAIL_FROM=os.getenv("MAIL_FROM", ""),
                          MAIL_PORT=587,
                          MAIL_SERVER="smtp.gmail.com",
                          MAIL_STARTTLS=True,
                          MAIL_SSL_TLS=False)

fm = FastMail(config)

async def enviar_confirmacao(email: str, nome: str):
    mensagem = MessageSchema(
        subject="Matricula confirmada",
        recipients=[NameEmail(name=nome, email=email)],
        body=f"<h1>Olá, {nome}!</h1><p>É com muito prazer que informamos a confirmação de sua matricula.</p>",
        subtype=MessageType.html,
    )
    await fm.send_message(mensagem)