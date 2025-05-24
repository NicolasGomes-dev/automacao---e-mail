# Importações
import imaplib
import email
from email.header import decode_header
import smtplib
from email.mime.text import MIMEText # Importação que permite criar e formatar msg de E-MAIL com conteúdo de texto.
import time

# Configurações
IMAP_SERVER ='imap.gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_ACCOUNT = 'seu_email@gmail.com'
EMAIL_PASSWORD = 'sua_senha_de_app'
IMAP_PORT = 993 # Porta padrão para conexões IMAP seguras (SSL/TLS)
SMPT_PORT = 587 #  Porta padrão para conexôes SMPT via STARTTLS (criptação)

def interpretar_mensagem(texto):
    """
    Função simples de interpretação de conteúdo.
    Pode ser expandida para usar modelos de NLP.
    """
    if 'preco' in texto.lower():
        return "Olá! O preço atual é R$100."
    elif 'horario' in texto.lower():
        return "Funcionamos de segunda a sexta, das 9h ás 18h."
    else:
        return "Obrigado pela sua mensagem! Em breve retornaremos."

def responder_email(destinatario, assunto, corpo):
    """
    Envia a resposta automática.
    """
    msg = MIMEText(corpo)
    msg['From'] = EMAIL_ACCOUNT
    msg['To'] = destinatario
    msg['Subject'] = f"Re: {assunto}"

    with smtplib.SMPT(SMTP_SERVER, SMPT_PORT) as server:
        server.starttls()
        server.login(EMAIL_ACCOUNT, destinatario, msg.as_string())
        print(f"Resposta enviada para: {destinatario}")