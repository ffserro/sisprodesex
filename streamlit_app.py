import streamlit as st
from config import firebaseConfig
import pyrebase

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

'''
def criar_usuario():
	criar_usuario = st.form('Criar um novo usuário')
	email = criar_usuario.text_input("Email", "", placeholder=None, disabled=False)
	senha = criar_usuario.text_input("Senha", type="password")
'''



#Resetar a senha
'''def reseta_senha():
	if authentication_status:
		try:
			if authenticator.reset_password(username, 'Reset password'):
				st.success('Password modified successfully')
		except Exception as e:
			st.error(e)
		atualiza_dados()

#Adicionar usuário
def adiciona_usuario():
	try:
		if authenticator.register_user('Register user', preauthorization=False):
			st.success('User registered successfully')
	except Exception as e:
		st.error(e)
	atualiza_dados()

#Esqueci a senha:
def esqueci_senha():
	try:
	    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
	    if username_forgot_pw:
	        st.success('New password sent securely')
	        # Random password to be transferred to user securely
	    elif username_forgot_pw == False:
	        st.error('Username not found')
	except Exception as e:
	    st.error(e)
	atualiza_dados()

#Esqueci o usuário:
def esqueci_usuario():
	try:
	    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
	    if username_forgot_username:
	        st.success('Username sent securely')
	        # Username to be transferred to user securely
	    elif username_forgot_username == False:
	        st.error('Email not found')
	except Exception as e:
	    st.error(e)
	atualiza_dados()


#Alterar dados dos usuários:
def altera_dados():
	if authentication_status:
		try:
			if authenticator.update_user_details(username, 'Update user details'):
				st.success('Entries updated successfully')
		except Exception as e:
			st.error(e)
		atualiza_dados()

#atualizar arquivo de usuários:
def atualiza_dados():
	with open('./config.yaml', 'w') as file:
		yaml.dump(config, file, default_flow_style=False)'''
#def admin():
	#st.title('Admin page')


#def default():
#	st.title('Teste')

#name, authentication_status, username = authenticator.login('SISPRODESEX', 'main')
login_form = st.form('Login')
login_form.subheader('SISPRODESEX')
email = login_form.text_input('Email').lower()
st.session_state['email'] = email
password = login_form.text_input('Senha', type='password')
if login_form.form_submit_button('Entrar'):
	try:
		print(1)
		user = auth.sign_in_with_email_and_password(email, password)
		print(2)
		st.session_state['username'] = db.child('usuarios').order_by_child('email').equal_to(email).get().each()[0].val()['usuario']
		print(3)
		st.session_state['authentication_status'] = True
		print(4)
		if st.session_state['username'] == 'admin':
			#admin()
			'''st.session_state.runpage = admin
			st.session_state.runpage()
			st.experimental_rerun'''
		print(5)

	except Exception as ex:
		st.write(type(ex).__name__)
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