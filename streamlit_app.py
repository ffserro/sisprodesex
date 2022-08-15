import streamlit_authenticator as stauth
import streamlit as st
import pyyaml as yaml

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#Resetar a senha
def reseta_senha():
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
		yaml.dump(config, file, default_flow_style=False)

def default():
	st.title('Teste')

name, authentication_status, username = authenticator.login('SISPRODESEX', 'main')

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
