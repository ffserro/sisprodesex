import streamlit as st
from streamlit_app import auth
from utilidades import nav_page

if 'authentication_status' not in st.session_state:
	st.session_state['authentication_status'] = None

if st.session_state['authentication_status'] == True:
    if st.session_state['username'] == 'admin':
        st.markdown("# Cadastro de usuários")
        st.sidebar.markdown("#")
        if st.session_state['message']:
            st.success(st.session_state['message'])
        with st.form("Cadastro"):
            st.write("Novo Usuário")
            novo_email = st.text_input('Insira o email')
            nova_senha = st.text_input('Insira a senha', type='password')
            repetir_nova_senha = st.text_input('Repita a senha', type='password')


            enviado = st.form_submit_button("Enviar")
            if enviado:
                if '@' not in novo_email:
                    st.warning('Insira um email válido')
                elif nova_senha != repetir_nova_senha:
                    st.warning('As senhas não conferem')
                else:
                    st.session_state['message'] = 'Cadastro realizado com sucesso'
                    auth.create_user_with_email_and_password(novo_email, nova_senha)
                    nav_page('Cadastro')