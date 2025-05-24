
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
SMTP_PORT = 587 #  Porta padrão para conexôes SMPT via STARTTLS (criptação)

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

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, destinatario, msg.as_string())
        print(f"Resposta enviada para: {destinatario}")

def verifica_emails():
    """
    Conecta na caixa de entrada e verifica novos e-mails.
    """
    with imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT) as mail:
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN)')
        if status != "OK":
            print("Nenhumn e-mail novo.")
            return
        for num in messages[0].split():
            status, data = mail.fetch(num, '(RFC822)')
            if status != "OK":
                continue
            
            msg = email.message_from_bytes(data[0][1])
            assunto, encoding = decode_header(msg.get("from"))[1]
            if isinstance(assunto, bytes):
                assunto = assunto.decode(encoding if encoding else "utf-8")
            remetente = email.utils.parseaddr(msg.get("From"))[1]

            #pega o corpo do e-mail
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        corpo = part.get_payload(decode=True).decode()
                        break
            else:
                corpo = msg.get_payload(decode=True).decode()

            resposta = interpretar_mensagem(corpo)
            responder_email(remetente, assunto, resposta)

            # Marca como lido
            mail.store(num, + 'FLAGS', '\\Seen')
        