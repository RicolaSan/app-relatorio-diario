import streamlit as st
from email_utils import enviar_relatorio
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página para modo mobile
st.set_page_config(page_title="Report Diário", page_icon="�", layout="centered")

# Estilização CSS personalizada para visual elegante e compacto
st.markdown("""
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            max-width: 600px;
        }
        h1 {
            font-size: 1.8rem !important;
            text-align: center;
            color: #2c3e50;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            height: 3em;
            font-weight: bold;
            background-color: #28a745;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #218838;
            color: white;
        }
        .css-1544g2n {
            padding: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📝 Report de Atividades")

# Configurações de Email (oculto por padrão para limpeza visual)
with st.expander("⚙️ Configurar Email"):
    email_remetente = st.text_input("Seu Email", value=os.getenv("EMAIL_REMETENTE", ""))
    senha_remetente = st.text_input("Senha de App", type="password", value=os.getenv("SENHA_REMETENTE", ""))
    email_supervisor = st.text_input("Email Supervisor", value=os.getenv("EMAIL_SUPERVISOR", ""))

# Seleção de método de entrada simplificada
metodo = st.segmented_control("Capturar Imagem", ["📸 Câmera", "📁 Galeria"], default="📸 Câmera")

foto = None
if metodo == "📸 Câmera":
    foto = st.camera_input("Tire a foto", label_visibility="collapsed")
else:
    foto = st.file_uploader("Selecione a imagem", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if foto:
    st.markdown("---")
    st.caption("✅ Imagem carregada")
    
    with st.form("form_envio", clear_on_submit=True):
        st.subheader("Detalhes")
        titulo = st.text_input("Título", placeholder="O que você fez?")
        descricao = st.text_area("Descrição", placeholder="Detalhes adicionais...", height=100)
        
        submitted = st.form_submit_button("🚀 Enviar Report")
        
        if submitted:
            if not titulo:
                st.warning("⚠️ O título é obrigatório.")
            elif not email_remetente or not senha_remetente:
                st.error("⚠️ Configure os emails antes de enviar.")
            else:
                with st.spinner("Enviando..."):
                    sucesso, msg = enviar_relatorio(
                        email_supervisor, titulo, descricao, foto, email_remetente, senha_remetente
                    )
                    if sucesso:
                        st.balloons()
                        st.success("Enviado com sucesso!")
                    else:
                        st.error(f"Erro: {msg}")
