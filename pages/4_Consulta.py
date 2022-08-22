import streamlit as st
from Logout import db, auth
import streamlit as st
import pandas as pd 
import numpy as np
from utilidades import nav_page
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="wide", initial_sidebar_state="expanded", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
elif st.session_state['origem'] == 'admin':
    nav_page('Cadastro')
else:
    st.sidebar.title('Consulta')
    st.sidebar.write('Esta página se destina à consulta da situação dos itens cadastrados e enviados, bem como ao histórico dos itens próprios já recebidos pelo DepSMRJ.')
    
    query = db.child('itens').get().val().values()

    df_itens = pd.DataFrame()
    for i in query:
        df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)
    
    df = df_itens[df_itens.origem == st.session_state['origem']]

    if len(df) == 0:
        st.title('Parece que você ainda não cadastrou nenhum item em excesso para destinação...')
        st.write('Por favor, se dirija a aba "Cadastro" para inserir novos itens.')
        st.stop()

    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df[['data_cadastro', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem', 'data_envio', 'data_recebimento']])

    #customize gridOptions
    gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    gb.configure_auto_height(True)
    gb.configure_pagination()
    gb.configure_column("data_cadastro", 'Data Cadastro', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
    gb.configure_column("data_envio", 'Data Envio', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
    gb.configure_column("data_recebimento", 'Data Recebimento', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
    gb.configure_column("pi", 'PI')
    gb.configure_column("nome", 'Nome do item')
    gb.configure_column("descricao",'Descrição')
    gb.configure_column("lvad", 'LVAD')
    gb.configure_column("preco_unitario", 'Preço Unitário', type=["customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='sum')
    gb.configure_column("quantidade", 'Quantidade', type=["numericColumn"], aggFunc='max')
    gb.configure_column("situacao", 'Situação')
    gb.configure_column("uf", 'UF')
    gb.configure_column("origem",'Origem')


    gb.configure_side_bar()

    gb.configure_selection('multiple')
    gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)

    gb.configure_pagination(paginationAutoPageSize=True)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    st.title('Consulta de itens em excesso')

    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        fit_columns_on_grid_load = True,
        data_return_mode='FILTERED', 
        update_mode='GRID_CHANGED',
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        theme='streamlit'    
        )