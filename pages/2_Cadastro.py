import streamlit as st
from streamlit_app import auth
from utilidades import nav_page
from datetime import datetime

def clear_form():
    for i in ['eml', 'snh', 'nvs', 'pii', 'nmi', 'lvi', 'dsi', 'qti', 'vli']:
        st.session_state[i] = ''

if 'authentication_status' not in st.session_state:
	st.session_state['authentication_status'] = None

if st.session_state['authentication_status'] == True:
    if st.session_state['username'] == 'admin':
        st.markdown("# Cadastro de usuários")
        st.sidebar.markdown("# Cadastro")
        if 'message' in st.session_state and st.session_state['message'] != '':
            st.success(st.session_state['message'])
            st.session_state['message'] = ''
        with st.form("Cadastro"):
            st.write("Novo Usuário")
            novo_email = st.text_input('Insira o email', key='eml')
            nova_senha = st.text_input('Insira a senha', type='password', key='snh')
            repetir_nova_senha = st.text_input('Repita a senha', type='password', key='nvs')


            enviado = st.form_submit_button("Enviar", on_click=clear_form)
            if enviado:
                if '@' not in novo_email:
                    st.warning('Insira um email válido')
                elif nova_senha != repetir_nova_senha:
                    st.warning('As senhas não conferem')
                else:
                    st.session_state['message'] = 'Cadastro realizado com sucesso'
                    auth.create_user_with_email_and_password(novo_email, nova_senha)
                    nav_page('Cadastro')

    else:
        st.markdown("# Cadastro de itens")
        st.sidebar.markdown("# Cadastro")
        if 'message' in st.session_state and st.session_state['message'] != '':
            st.success(st.session_state['message'])
        with st.form("Cadastro de excessos"):
            st.write("Novo item")
            pi_item = st.text_input('Insira PI', key='pii')
            nome_item = st.text_input('Insira o nome do item', key='nmi')
            desc_item = st.text_area('Descrição do item', key='dsi')
            f3, f4 = st.columns([1,1])
            with f3:
                lvad_item = st.text_input('LVAD', key='lvi')
            with f4:
                uf_item = st.selectbox('UF', ('', 'Unidade', 'Quilogramas', 'Litros', 'Fardos'))
            f1, f2 = st.columns([1,1])
            with f1:
                quant_item = st.number_input('Quantidade', min_value=0, key='qti')
            with f2:
                preco_unit = st.number_input('Valor unitário', min_value=0.00,step = 1.00, format='%.2f', key='vli')


            enviado = st.form_submit_button("Cadastrar", on_click=clear_form)
            if enviado:
                if pi_item == '' or nome_item == '' or desc_item == '' or lvad_item == '' or quant_item == '' or preco_unit == '':
                    st.warning('Por favor, preencha todos os campos')
                else:
                    st.session_state['message'] = 'Cadastro realizado com sucesso'
                    db.child('itens').push(
                        {'id':(list(db.child('itens').order_by_child('id').limit_to_last(1).get().val().values())[0]['id']) + 1,
                        'pi':pi_item,
                        'nome':nome_item,
                        'descricao':desc_item,
                        'lvad':lvad_item,
                        'data_envio':datetime.now().strftime("%d/%m/%Y"),
                        'preco_unitario':preco_unit,
                        'quantidade':quant_item,
                        'situacao':'cadastrado',
                        'uf':uf_item,
                        'origem':st.session_state['username']}
                    )
                    nav_page('Cadastro')