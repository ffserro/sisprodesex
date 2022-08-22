import streamlit as st
from Logout import db, auth
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
from datetime import datetime

st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", initial_sidebar_state="expanded", menu_items=None)

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

    kpi1.metric(
        label="Quantidade de itens cadastrados",
        value=len(df_itens)
    )

    kpi2.metric(
        label="Quantidade de itens recebidos pelo DepSMRJ",
        value=len(df_itens[df_itens.data_recebimento != ''])
    )

    kpi3.metric(
        label="Total de Excessos Destinados",
        value='R$ {:.2f}'.format(sum(df_itens.preco_unitario * df_itens.quantidade))
    )

    st.dataframe(df_itens.set_index('id'))

    df_xlsx = to_excel(df_itens[['data_cadastro', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem', 'data_envio', 'data_recebimento']])
    st.download_button(label='Baixar relatório', data=df_xlsx , file_name= f'Relatorio{datetime.now().year}{datetime.now().month}{datetime.now().day}.xlsx')