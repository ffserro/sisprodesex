import streamlit as st
from Logout import auth
from utilidades import nav_page
import pandas as pd
import numpy as np
st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", initial_sidebar_state="expanded", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:
    st.markdown("# Seja bem vindo ao PRODESEX")
    st.sidebar.markdown("# Página principal")
    st.sidebar.write('Para navegar pelas funcionalidades do sistema, por favor clique no link para ser redirecionado para umas das abas que são mostradas acima.')

    st.write('''
    O Sistema de Apoio ao Programa de Destinação de Excessos é uma sugestão de melhoria para os processos de intendência do Grupo H do CApA-2022, composto pelos:
    - 1T(IM) Sacramento
    - 1T(IM) Raí
    - 1T(IM) Matheus Bispo
    - 1T(IM) Sêrro
    - 1T(QC-IM) Ludmilla
    ''')


























