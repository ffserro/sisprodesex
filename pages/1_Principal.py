import streamlit as st
from Logout import auth
from utilidades import nav_page
import pandas as pd
import numpy as np
import webbrowser
st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", initial_sidebar_state="expanded", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:
    st.markdown("# Seja bem vindo ao SISPRODESEX")
    st.sidebar.markdown("# Página principal")
    st.sidebar.write('Para navegar pelas funcionalidades do sistema, por favor clique em um dos links mostrados acima para ser redirecionado para umas das abas.')

    st.write('''
    O Sistema de Apoio ao Programa de Destinação de Excessos é uma sugestão de melhoria para os processos de intendência do Grupo H do CApA-2022, composto pelos:
    - 1T(IM) Sacramento
    - 1T(IM) Matheus Bispo
    - 1T(IM) Raí
    - 1T(IM) Sêrro
    - 1T(QC-IM) Ludmila Patrício
    ''')
    st.write('''
    O propósito maior deste sistema ora apresentado é tornar mais eficientes a identificação e o controle dos itens de sobressalentes classificados como excesso, desde a sua origem nos diversos Órgãos de Distribuição localizados em diferentes regiões do país, até sua posterior distribuição pelo Depósito de Sobressalentes da Marinha no Rio de Janeiro.
    ''')
    st.write('''
    Esperamos com esse trabalho contribuir com a eficiência do SAbM e também caminhar no sentido de consolidar a cultura Data-driven no contexto administrativo da Marinha do Brasil.
    ''')
    st.write('''Confira abaixo as normas que regem o SAbM e as sugestões formuladas pelo grupo:''')
    f1, f2, f3 = st.columns(3)
    with f1:
        st.write(f'''
            <a target="_self" href="https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Documentos%2FSGM-401.pdf?alt=media&token=55abeb30-8758-4db2-8052-bcfab7cbde00">
                <button>
                    SGM-201
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
    with f2:
        if st.button('ABASTCMARINST'):
            webbrowser.open_new_tab('https://google.com')
    with f3:
        if st.button('Sugestões do grupo'):
            webbrowser.open_new_tab('https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Documentos%2FNorma%20Grupo%20H.docx.pdf?alt=media&token=e61f5f01-d2d9-4527-bb4e-07540ce22348')
























