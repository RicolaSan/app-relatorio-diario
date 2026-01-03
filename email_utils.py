import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os

def enviar_relatorio(email_supervisor, titulo, descricao, imagem_bytes, email_remetente, senha_remetente):
    """
    Envia um email com o relatório e a foto anexada.
    """
    msg = MIMEMultipart()
    msg['Subject'] = f"Relatório: {titulo}"
    msg['From'] = email_remetente
    msg['To'] = email_supervisor

    # Preparar lista de destinatários (suporta múltiplos emails separados por vírgula)
    if ',' in email_supervisor:
        destinatarios = [e.strip() for e in email_supervisor.split(',')]
    else:
        destinatarios = [email_supervisor]

    # Corpo do email
    texto = f"""
    Olá,

    Segue novo relatório de atividade da equipe.

    Título: {titulo}
    Descrição: {descricao}

    A foto da atividade está anexada.
    """
    msg.attach(MIMEText(texto, 'plain'))

    # Anexar a imagem
    if imagem_bytes:
        image = MIMEImage(imagem_bytes.read(), name="atividade.jpg")
        msg.attach(image)

    # Enviar email via Gmail (usando porta 587 - TLS, que evita bloqueios de firewall)
    context = ssl.create_default_context()
    try:
        # Usando SMTP com STARTTLS na porta 587 em vez de SSL na 465
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo() # Identificação inicial
            server.starttls(context=context) # Atualiza conexão para segura
            server.ehlo() # Reidentificação após segurança
            server.login(email_remetente, senha_remetente)
            server.sendmail(email_remetente, destinatarios, msg.as_string())
        return True, "Email enviado com sucesso!"
    except Exception as e:
        return False, f"Erro ao enviar email: {str(e)}"
