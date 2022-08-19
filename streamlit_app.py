import streamlit as st
from utilidades import nav_page
from config import config
import pyrebase

st.set_page_config(page_title='SISPRODESEX', page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

if 'authentication_status' not in st.session_state:
	st.session_state['authentication_status'] = None


def criar_usuario():
	criar_usuario = st.form('Criar um novo usuário')
	email = criar_usuario.text_input("Email", "", placeholder=None, disabled=False)
	senha = criar_usuario.text_input("Senha", type="password")

def admin():
	st.experimental_rerun()
	st.title('Admin page')

if st.session_state['authentication_status'] != True:
	login_form = st.form('Login')
	login_form.subheader('SISPRODESEX')
	email = login_form.text_input('Email')
	st.session_state['email'] = email
	password = login_form.text_input('Senha', type='password')
	if login_form.form_submit_button('Entrar'):
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			st.session_state['username'] = list(db.child('usuarios').order_by_child('email').equal_to(st.session_state['email']).get().val().values())[0]['usuario']
			st.session_state['authentication_status'] = True
			nav_page('Principal')
		except Exception as ex:
			st.write(type(ex).__name__)
			st.write(ex.args)
			st.warning('O email ou senha fornecidos são inválidos.')