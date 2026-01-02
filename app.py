import streamlit as st
from email_utils import enviar_relatorio
import os
from dotenv import load_dotenv
import extra_streamlit_components as stx
import datetime

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página para modo mobile
st.set_page_config(page_title="Report Diário", page_icon="📝", layout="centered")

# --- Gerenciador de Cookies ---
# Removido o cache para evitar o erro de widgets
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()

# --- Lógica de Login ---
if 'logado' not in st.session_state:
    st.session_state['logado'] = False

# Tenta recuperar sessão via cookie se ainda não estiver logado
if not st.session_state['logado']:
    cookie_token = cookie_manager.get(cookie="auth_token")
    if cookie_token == "valid_token_1234":
        st.session_state['logado'] = True

if not st.session_state['logado']:
    # Injeta CSS específico para a tela de login ficar compacta e centralizada
    st.markdown("""
        <style>
            .stApp {
                background-color: #f0f2f6;
            }
            [data-testid="stForm"] {
                background-color: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                max-width: 350px;
                margin: 0 auto;
            }
            .login-header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .login-header h1 {
                font-size: 1.8rem;
                color: #1f2937;
                margin: 0;
            }
            .login-header p {
                color: #6b7280;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # Container centralizado verticalmente (simulação visual)
    st.markdown('<div class="login-header"><h1>🔒 Acesso</h1><p>Identifique-se para continuar</p></div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        usuario = st.text_input("Usuário", placeholder="Seu usuário")
        senha = st.text_input("Senha", type="password", max_chars=4, placeholder="****")
        
        st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
        submit_login = st.form_submit_button("Entrar", use_container_width=True)
        
        if submit_login:
            if usuario == "admin" and senha == "1234":
                st.session_state['logado'] = True
                # Salva cookie válido por 30 dias
                expires = datetime.datetime.now() + datetime.timedelta(days=30)
                cookie_manager.set("auth_token", "valid_token_1234", expires=expires)
                st.rerun()
            else:
                st.error("❌ Dados incorretos")
    
    st.stop()

# Botão de Logout (Opcional, no topo ou sidebar)
if st.sidebar.button("Sair 🚪"):
    st.session_state['logado'] = False
    cookie_manager.delete("auth_token")
    st.rerun()
# -----------------------

# Estilização CSS personalizada para visual elegante e compacto
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 500px;
        }
        h1 {
            font-size: 1.6rem !important;
            text-align: center;
            color: #1f2937;
            margin-bottom: 1rem;
        }
        
        /* Estilo do botão de Enviar (Verde e largo) */
        .stButton>button {
            width: 100%;
            border-radius: 25px;
            height: 3.5em;
            font-weight: 600;
            background-color: #10b981; /* Verde esmeralda moderno */
            color: white;
            border: none;
            box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.4);
            transition: all 0.2s;
        }
        .stButton>button:hover {
            background-color: #059669;
            transform: translateY(-2px);
            box-shadow: 0 6px 8px -1px rgba(16, 185, 129, 0.5);
        }

        /* Hack para trocar o texto "Take Photo" para "Tirar Foto" */
        div[data-testid="stCameraInput"] button[aria-label="Take photo"] {
            color: transparent !important;
            position: relative;
        }
        div[data-testid="stCameraInput"] button[aria-label="Take photo"]::after {
            content: "📷 Tirar Foto";
            color: #31333f;
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            font-size: 16px;
            font-weight: bold;
            white-space: nowrap;
        }

        /* Ajuste simples para o File Uploader */
        [data-testid='stFileUploader'] {
            width: 100%;
        }


        
        /* Melhorar inputs de texto */
        .stTextInput input, .stTextArea textarea {
            border-radius: 10px;
            border: 1px solid #d1d5db;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #10b981;
            box-shadow: 0 0 0 1px #10b981;
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
    st.caption("Qualidade padrão do navegador.")
    foto = st.camera_input("Tire a foto", label_visibility="collapsed")
else:
    st.caption("Use para fotos da galeria ou câmera nativa (Melhor qualidade).")
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
