import streamlit as st
from Logout import db, auth
import pandas as pd
from streamlit_elements import elements, mui
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from datetime import datetime

st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="wide", initial_sidebar_state="collapsed", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
elif st.session_state['origem'] == 'admin':
    nav_page('Cadastro')
else:
    st.sidebar.title('Relatório')
    st.sidebar.write('''
    Esta página é destinada a emissão de relatórios no formato .xlsx (excel), que consolidam as informações de todos os Órgãos de Distribuição e do DepSMRJ.
    ''')

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Relatório_SISPRODESEX')
        workbook = writer.book
        worksheet = writer.sheets['Relatório_SISPRODESEX']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.save()
        processed_data = output.getvalue()
        return processed_data

    query = db.child('itens').get().val().values()

    df_itens = pd.DataFrame()
    for i in query:
        df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)

    st.title('Emitir Relatório')

    kpi1, kpi2, kpi3 = st.columns(3)

    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
        justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
        justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

    kpi1.metric(
        label="Quantidade de itens cadastrados",
        value=len(df_itens)
    )

    kpi2.metric(
        label="Recebidos pelo DepSMRJ",
        value=len(df_itens[df_itens.data_recebimento != ''])
    )

    kpi3.metric(
        label="Total de Excessos Destinados",
        value='R$ {:.2f}'.format(sum(df_itens.preco_unitario * df_itens.quantidade)).replace('.',',')
    )

    gb = GridOptionsBuilder.from_dataframe(df_itens[['data_cadastro', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem', 'data_envio', 'data_recebimento']])

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

    gb.configure_selection('single')
    

    gb.configure_pagination(paginationAutoPageSize=True)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    grid_response = AgGrid(
        df_itens, 
        gridOptions=gridOptions,
        fit_columns_on_grid_load = True,
        data_return_mode='FILTERED', 
        update_mode='GRID_CHANGED',
        allow_unsafe_jscode=True,
        theme='streamlit'    
        )


    df_itens = pd.DataFrame(grid_response['data'])
    df_xlsx = to_excel(df_itens[['data_cadastro', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem', 'data_envio', 'data_recebimento', 'data_descaracterizacao', 'data_pronto_descaracterizacao','data_alienacao', 'num_lote', 'num_leilao', 'nome_om']])

    st.download_button(label='Baixar relatório', data=df_xlsx , file_name= f'Relatorio{datetime.now().year}{datetime.now().month}{datetime.now().day}.xlsx')