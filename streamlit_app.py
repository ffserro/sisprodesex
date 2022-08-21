import streamlit as st
from utilidades import nav_page
#from config import config
import pyrebase
st.set_page_config(page_title='SISPRODESEX', page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)

firebase = pyrebase.initialize_app(st.secrets.CONFIG_KEY)
auth = firebase.auth()
db = firebase.database()

st.session_state['authentication_status'] = False

login_form = st.form('Login')
login_form.markdown("<h1 style='text-align: center;'>SISPRODESEX</h1>", unsafe_allow_html=True)
login_form.markdown("<img style='display: block; margin-left: auto; margin-right: auto; width:50%;' src='https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Imagens%2Fdepsmrj.png?alt=media&token=bc3a82e2-776e-4786-8968-bd1e58fe5a60' alt='DepSMRJ' width='500'>", unsafe_allow_html=True)
email = login_form.text_input('Email')
st.session_state['email'] = email
password = login_form.text_input('Senha', type='password')
if login_form.form_submit_button('Entrar'):
	try:
		user = auth.sign_in_with_email_and_password(email, password)
		query = list(db.child('usuarios').order_by_child('email').equal_to(st.session_state['email']).get().val().values())[0]
		st.session_state['username'] = query['usuario']
		st.session_state['origem'] = query['origem']
		st.session_state['authentication_status'] = True
		nav_page('Principal')
	except Exception as ex:
		st.write(type(ex).__name__)
		st.write(ex.args)
		st.warning('O email ou senha fornecidos são inválidos.')