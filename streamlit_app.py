import streamlit as st
from utilidades import nav_page
from config import firebaseConfig
import pyrebase

st.set_page_config(page_title='SISPRODESEX', page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
url = 'https://ffserro-streamlit-example-streamlit-app-nduyu5.streamlitapp.com/'
firebase = pyrebase.initialize_app(firebaseConfig)
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
	email = login_form.text_input('Email').lower()
	st.session_state['email'] = email
	password = login_form.text_input('Senha', type='password')
	if login_form.form_submit_button('Entrar'):
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			st.session_state['username'] = db.child('usuarios').child('usuario').get().val()[db.child('usuarios').child('email').get().val().index(email)]
			st.session_state['authentication_status'] = True
			if st.session_state['username'] == 'admin':
				nav_page('Principal')

				'''st.session_state.runpage = admin
				st.session_state.runpage()
				st.experimental_rerun()'''

		except Exception as ex:
			st.write(type(ex).__name__)
			st.write(ex.args)
			st.warning('O email ou senha fornecidos são inválidos.')
'''
if st.session_state["authentication_status"]:
	authenticator.logout('Sair', 'main')
	st.title(f'Seja bem vindo,  *{st.session_state["name"]}*')
	if st.session_state['name'] == 'admin':
		pag = st.selectbox('Serviços disponíveis', ['-', 'Resetar a senha','Adicionar usuário', 'Trocar a senha', 'Trocar o usuário', 'Alterar dados'])
		if pag == 'Resetar a senha':
			reseta_senha()
		elif pag == 'Adicionar usuário':
			adiciona_usuario()
		elif pag == 'Trocar a senha':
			esqueci_senha()
		elif pag == 'Trocar o usuário':
			esqueci_usuario()
		elif pag == 'Alterar dados':
			altera_dados()
	else:
		pass
	
elif st.session_state["authentication_status"] == False:
    st.error('Usuário ou senha incorretos')
elif st.session_state["authentication_status"] == None:
	pass
'''