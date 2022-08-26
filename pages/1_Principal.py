import streamlit as st
from Logout import auth
from utilidades import nav_page
import pandas as pd
import numpy as np
st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", initial_sidebar_state="expanded", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:
    st.markdown("# Seja bem vindo ao SISPRODESEX")
    st.sidebar.markdown("# Página principal")
    st.sidebar.write('Para navegar pelas funcionalidades do sistema, por favor clique em um dos links mostrados acima para ser redirecionado para umas das abas.')

    st.write('''
    O Subsistema do Programa de Destinação de Excessos é uma sugestão de melhoria para os processos de intendência do Grupo H do CApA-2022, composto pelos:
    - 1ºTen (IM) Sacramento
    - 1ºTen (IM) Matheus Bispo
    - 1ºTen (IM) Raí
    - 1ºTen (IM) Sêrro
    - 1ºTen (QC-IM) Ludmila Patrício
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
            <a target="_blank" 
            style="color:black; text-decoration:none"
            href="https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Documentos%2FSGM-201-Rev-7.pdf?alt=media&token=63e2fece-7f2f-4b11-ac33-51728282bdef">
                <button class = "css-1cpxqw2 edgvbvh5">
                    SGM-201
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
    with f2:
        st.write(f'''
            <a target="_blank"
            style="color:black; text-decoration:none"
            href="https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Documentos%2FABASTCMARINST-20-01A---ANEXO-D---Sobressalentes.pdf?alt=media&token=243f6c51-5f46-484b-8fdd-584716f740b8">
                <button class = "css-1cpxqw2 edgvbvh5">
                    ABASTCMARINST
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
    with f3:
        st.write(f'''
            <a target="_blank" 
            style="color:black; text-decoration:none"
            href="https://firebasestorage.googleapis.com/v0/b/prodesex-8e59f.appspot.com/o/Documentos%2FCorpo%20do%20Trabalho.pdf?alt=media&token=5a26fa6b-b7a7-4e4d-adee-867fc88c162d">
                <button class = "css-1cpxqw2 edgvbvh5">
                    Sugestões do grupo
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )
        























