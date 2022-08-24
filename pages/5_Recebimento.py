import streamlit as st
from Logout import db, auth
from utilidades import nav_page
import streamlit as st
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from datetime import datetime
st.set_page_config(page_title='SISPRODESEX', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="wide", initial_sidebar_state="expanded", menu_items=None)

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
elif st.session_state['origem'] != 'DEPSMRJ':
    nav_page('Envio')
else:
    st.sidebar.title('Recebimento')
    st.sidebar.write('Esta página se destina à confirmação do recebimento por parte do DepSMRJ dos itens que se encontravam em trânsito.')
    modulo = st.sidebar.selectbox('Selecione a funcionalidade desejada:', ['Recebimento', 'Descaracterização', 'Pronto da descaracterização', 'Distribuição', 'Venda'])
    
    query = db.child('itens').get().val().values()

    df_itens = pd.DataFrame()
    for i in query:
        df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)

    if modulo == 'Recebimento':
        df = df_itens[df_itens.situacao == 'Em trânsito']

        if len(df) == 0:
            st.title('Parece que não existem itens aguardando para serem recebidos pelo DepSMRJ...')
            st.write('Por favor acompanhe o andamento dos itens enviados na aba "Consulta".')
            st.stop()

        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df[['data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

        #customize gridOptions
        gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_auto_height(True)
        gb.configure_pagination()
        gb.configure_column("data_envio", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
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



        st.write('# Recebimento dos itens enviados')

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            fit_columns_on_grid_load = True,
            data_return_mode='FILTERED', 
            update_mode='GRID_CHANGED',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            theme='streamlit'    
            )


        enviar = st.button('Receber itens enviados')

        if enviar:
            ids = [i['id'] for i in grid_response['selected_rows']]
            for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
                db.child('itens').child(i).update({'situacao':'Recebido', 'data_recebimento':datetime.now().strftime("%d/%m/%Y")})
            nav_page('Recebimento')

    elif modulo == 'Descaracterização':
        df = df_itens[df_itens.situacao == 'Recebido']

        if len(df) == 0:
            st.title('Parece que não existem itens aguardando para serem recebidos pelo DepSMRJ...')
            st.write('Por favor acompanhe o andamento dos itens enviados na aba "Consulta".')
            st.stop()

        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df[['data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

        #customize gridOptions
        gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_auto_height(True)
        gb.configure_pagination()
        gb.configure_column("data_envio", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
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



        st.write('# Recebimento dos itens enviados')

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            fit_columns_on_grid_load = True,
            data_return_mode='FILTERED', 
            update_mode='GRID_CHANGED',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            theme='streamlit'    
            )


        enviar = st.button('Descaracterizar itens recebidos')

        if enviar:
            ids = [i['id'] for i in grid_response['selected_rows']]
            for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
                db.child('itens').child(i).update({'situacao':'Em descaracterização', 'data_recebimento':datetime.now().strftime("%d/%m/%Y")})
            nav_page('Recebimento')

    elif modulo == 'Pronto da descaracterização':
        df = df_itens[df_itens.situacao == 'Em descaracterização']

        if len(df) == 0:
            st.title('Parece que não existem itens aguardando para serem recebidos pelo DepSMRJ...')
            st.write('Por favor acompanhe o andamento dos itens enviados na aba "Consulta".')
            st.stop()

        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df[['data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

        #customize gridOptions
        gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_auto_height(True)
        gb.configure_pagination()
        gb.configure_column("data_envio", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
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



        st.write('# Recebimento dos itens enviados')

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            fit_columns_on_grid_load = True,
            data_return_mode='FILTERED', 
            update_mode='GRID_CHANGED',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            theme='streamlit'    
            )


        enviar = st.button('Descaracterizar itens recebidos')

        if enviar:
            ids = [i['id'] for i in grid_response['selected_rows']]
            for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
                db.child('itens').child(i).update({'situacao':'Descaracterizado', 'data_recebimento':datetime.now().strftime("%d/%m/%Y")})
            nav_page('Recebimento')



    elif modulo == 'Distribuição':
        df = df_itens[df_itens.situacao == 'Descaracterizado']

        if len(df) == 0:
            st.title('Parece que não existem itens aguardando para serem recebidos pelo DepSMRJ...')
            st.write('Por favor acompanhe o andamento dos itens enviados na aba "Consulta".')
            st.stop()

        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df[['data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

        #customize gridOptions
        gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_auto_height(True)
        gb.configure_pagination()
        gb.configure_column("data_envio", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
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



        st.write('# Recebimento dos itens enviados')

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            fit_columns_on_grid_load = True,
            data_return_mode='FILTERED', 
            update_mode='GRID_CHANGED',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            theme='streamlit'    
            )

        c1, c2 = st.columns(2)
        with c1:
            enviar = st.button('Fornecido para OM')
        with c2:
            vender = st.button('Vendido em leilão')

        if enviar:
            with st.form('distribuido'):
                nome_om = st.text_input('Digite o nome da OM que recebeu o item: ')
                distribuido = st.form_submit_button('Enviar')
                if distribuido:
                    try:
                        ids = [i['id'] for i in grid_response['selected_rows']]
                        for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
                            db.child('itens').child(i).update({'nome_OM':distribuido,'situacao':'Distribuído para OM', 'data_recebimento':datetime.now().strftime("%d/%m/%Y")})
                    except Exception err:
                        st.write(err)
                    nav_page('Recebimento')
        if vender:
            ids = [i['id'] for i in grid_response['selected_rows']]
            for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
                db.child('itens').child(i).update({'situacao':'Para venda', 'data_recebimento':datetime.now().strftime("%d/%m/%Y")})
            nav_page('Recebimento')

    elif modulo == 'Venda':
        df = df_itens[df_itens.situacao == 'Para venda']

        if len(df) == 0:
            st.title('Parece que não existem itens aguardando para serem recebidos pelo DepSMRJ...')
            st.write('Por favor acompanhe o andamento dos itens enviados na aba "Consulta".')
            st.stop()

        #Infer basic colDefs from dataframe types
        gb = GridOptionsBuilder.from_dataframe(df[['data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

        #customize gridOptions
        gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        gb.configure_auto_height(True)
        gb.configure_pagination()
        gb.configure_column("data_envio", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
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



        st.write('# Recebimento dos itens enviados')

        grid_response = AgGrid(
            df, 
            gridOptions=gridOptions,
            fit_columns_on_grid_load = True,
            data_return_mode='FILTERED', 
            update_mode='GRID_CHANGED',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            theme='streamlit'    
            )

        enviar = st.button('Leiloado')
        
