import streamlit as st
import pandas as pd


clientes = pd.read_csv('./cliente.csv')


st.sidebar.title('Menu')
paginaSelecionada = st.sidebar.selectbox('Selecione a página: ', ['Cadastro','Consulta'])

if paginaSelecionada == 'Cadastro':
    st.title('Incluir Cliente')

    with st.form(key='include_cliente', clear_on_submit=True):
        input_name = st.text_input(label='Insira o seu nome')
        input_age = st.number_input(label='Insira a sua idade', format='%d', step=1)
        input_occupation = st.selectbox(label='Selecione a sua profissao', options=['Desenvolvedor', 'Designer', 'Professor'])
        input_button_submit = st.form_submit_button(label='Enviar')

    if input_button_submit:
        nome = input_name
        idade = input_age
        profissao = input_occupation
        clientes = clientes.append(pd.DataFrame({'Nome':[nome], 'Idade':[idade], 'Profissao':[profissao]}))
        clientes.to_csv('./cliente.csv', index=False)
        st.success('Cliente cadastrado com sucesso.')

elif paginaSelecionada == 'Consulta':
    st.title('Consulta Clientes')
    st.table(clientes)