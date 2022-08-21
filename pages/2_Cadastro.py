import streamlit as st
from Logout import auth, db
from utilidades import nav_page
from datetime import datetime

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:
    if st.session_state['username'] == 'admin':
        st.markdown("# Cadastro de usuários")
        st.sidebar.markdown("# Cadastro")
        if 'message' in st.session_state and st.session_state['message'] != '':
            st.success(st.session_state['message'])
            st.session_state['message'] = ''
        with st.form("Cadastro", clear_on_submit=True):
            st.write("Novo Usuário")
            f1, f2 = st.columns([1,1])
            with f1:
                novo_usuario = st.text_input('Insira um nome de usuário', key='usr')
            with f2:
                indicativo = st.text_input('Insira o indicativo da OM', key='iom')
            novo_email = st.text_input('Insira o email', key='eml')
            nova_senha = st.text_input('Insira a senha', type='password', key='snh')
            repetir_nova_senha = st.text_input('Repita a senha', type='password', key='nvs')


            enviado = st.form_submit_button("Enviar")
            if enviado:
                if '@' not in novo_email:
                    st.warning('Insira um email válido')
                elif novo_usuario in [i['usuario'] for i in list(db.child('usuarios').get().val().values())]:
                    st.warning('Usuário já existe. Por favor escolha um novo nome de usuário.')
                elif nova_senha != repetir_nova_senha:
                    st.warning('As senhas não conferem')
                else:
                    st.session_state['message'] = 'Cadastro realizado com sucesso'
                    db.child('usuarios').push({
                        'email':novo_email,
                        'origem':indicativo.upper(),
                        'usuario':novo_usuario
                    })
                    auth.create_user_with_email_and_password(novo_email, nova_senha)
                    nav_page('Cadastro')

    else:
        st.markdown("# Cadastro de itens")
        st.sidebar.markdown("# Cadastro")
        if 'message' in st.session_state and st.session_state['message'] != '':
            st.success(st.session_state['message'])
        with st.form("Cadastro de excessos", clear_on_submit=True):
            st.write("Novo item")
            try:
                id_item = int(list(db.child('itens').order_by_child('id').limit_to_last(1).get().val().values())[0]['id']) + 1
            except:
                id_item = 0
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


            enviado = st.form_submit_button("Cadastrar")
            if enviado:
                if pi_item == '' or nome_item == '' or desc_item == '' or lvad_item == '' or quant_item == '' or preco_unit == '':
                    st.warning('Por favor, preencha todos os campos')
                else:
                    st.session_state['message'] = 'Cadastro realizado com sucesso'
                    db.child('itens').push(
                        {'id':id_item,
                        'pi':pi_item,
                        'nome':nome_item,
                        'descricao':desc_item,
                        'lvad':lvad_item,
                        'data_cadastro':datetime.now().strftime("%d/%m/%Y"),
                        'data_envio':'',
                        'data_recebimento':'',
                        'preco_unitario':preco_unit,
                        'quantidade':quant_item,
                        'situacao':'cadastrado',
                        'uf':uf_item,
                        'origem':st.session_state['username']}
                    )
                    nav_page('Cadastro')