import streamlit as st
import numpy as np
import pandas as pd

df = pd.read_csv('./bd_rosalvos.csv')

st.title('Página teste do Rosalvito')

with st.form('Inserir Fornecedores'):
    cnpj = st.text_input('CNPJ')
    nome_empresa = st.text_input('Nome da empresa')
    num_nf = st.text_input('Número da nota fiscal')
    data_nf = st.date_input('Data da nota fiscal')
    recebedor = st.text_input('Nome do recebedor')
    nip = st.text_input('NIP do recebedor')
    submeter = st.form_submit_button('Enviar')

if submeter:
    ins = pd.DataFrame([[cnpj, nome_empresa, num_nf, data_nf, recebedor, nip]])
    df = pd.concat([df, ins], axis=1, ignore_index=True)
    df.to_csv('./bd_rosalvos.csv')

st.dataframe(df)