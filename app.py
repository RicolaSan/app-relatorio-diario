import streamlit as st
from email_utils import enviar_relatorio
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente (se existirem)
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Relatório Diário", page_icon="📸")

st.title("📸 Report Diário da Equipe")
st.write("Tire uma foto da atividade e envie o relatório para o supervisor.")

# Passo 1: Configurações (Pode ser escondido ou movido para .env na produção)
with st.expander("⚙️ Configurações de Email (Preencha aqui ou no arquivo .env)"):
    email_remetente = st.text_input("Seu Email (Gmail)", value=os.getenv("EMAIL_REMETENTE", ""))
    senha_remetente = st.text_input("Sua Senha de App (Não é a senha normal)", type="password", value=os.getenv("SENHA_REMETENTE", ""))
    email_supervisor = st.text_input("Email do Supervisor", value=os.getenv("EMAIL_SUPERVISOR", ""))
    st.info("Para usar o Gmail, você precisa criar uma 'Senha de App' nas configurações de segurança do Google.")

# Passo 2: Câmera ou Upload
st.subheader("1. Capturar Atividade")

# Opção para escolher entre Câmera ou Upload (caso a câmera não funcione)
opcao_captura = st.radio("Como deseja capturar a imagem?", ["📸 Usar Câmera", "📁 Fazer Upload"], horizontal=True)

foto = None
if opcao_captura == "📸 Usar Câmera":
    foto = st.camera_input("Tire uma foto do que foi feito")
else:
    foto = st.file_uploader("Escolha uma imagem do seu dispositivo", type=['png', 'jpg', 'jpeg'])

# Passo 3: Detalhes e Envio
if foto:
    st.success("Foto capturada com sucesso!")
    st.subheader("2. Detalhes da Atividade")
    
    with st.form("form_relatorio"):
        titulo = st.text_input("Título da Atividade", placeholder="Ex: Troca de fita da impressora")
        descricao = st.text_area("Descrição do que foi feito", placeholder="Detalhe o processo realizado...")
        
        submitted = st.form_submit_button("✅ Confirmar e Enviar Relatório")
        
        if submitted:
            if not titulo or not descricao:
                st.error("Por favor, preencha o título e a descrição.")
            elif not email_remetente or not senha_remetente or not email_supervisor:
                st.error("Por favor, preencha as configurações de email acima.")
            else:
                with st.spinner("Enviando relatório..."):
                    # Rebobinar o ponteiro do arquivo de imagem para leitura
                    # A função enviar_relatorio espera o buffer, o streamlit já entrega um buffer
                    sucesso, mensagem = enviar_relatorio(
                        email_supervisor, 
                        titulo, 
                        descricao, 
                        foto, 
                        email_remetente, 
                        senha_remetente
                    )
                    
                    if sucesso:
                        st.balloons()
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
