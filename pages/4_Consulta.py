import streamlit as st
from streamlit_app import db, auth
from distutils import errors
from distutils.log import error
import streamlit as st
import pandas as pd 
import numpy as np
import altair as alt
from itertools import cycle
from utilidades import nav_page
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(layout="wide")

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:
    
    query = db.child('itens').get().val().values()

    df_itens = pd.DataFrame()
    for i in query:
        df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)
    
    df = df_itens[df_itens.origem == st.session_state['origem']]

    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df[['data_cadastro', 'data_envio', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem', 'data_recebimento']])

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

    st.title('Consulta de itens cadastrados')
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        fit_columns_on_grid_load = True,
        data_return_mode='FILTERED', 
        update_mode='GRID_CHANGED',
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        theme='streamlit'    
        )


    df_final = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected)

    st.write(df_itens)
    st.write(df_final)
    st.write(selected)
    st.write(selected_df)


    '''
    #Example controlers
    st.sidebar.subheader("St-AgGrid example options")

    sample_size = st.sidebar.number_input("rows", min_value=10, value=30)
    grid_height = st.sidebar.number_input("Grid height", min_value=200, max_value=800, value=300)

    return_mode = st.sidebar.selectbox("Return Mode", list(DataReturnMode.__members__), index=1)
    return_mode_value = DataReturnMode.__members__[return_mode]

    update_mode = st.sidebar.selectbox("Update Mode", list(GridUpdateMode.__members__), index=len(GridUpdateMode.__members__)-1)
    update_mode_value = GridUpdateMode.__members__[update_mode]

    #enterprise modules
    enable_enterprise_modules = st.sidebar.checkbox("Enable Enterprise Modules")
    if enable_enterprise_modules:
        enable_sidebar =st.sidebar.checkbox("Enable grid sidebar", value=False)
    else:
        enable_sidebar = False

    #features
    fit_columns_on_grid_load = st.sidebar.checkbox("Fit Grid Columns on Load")

    enable_selection=st.sidebar.checkbox("Enable row selection", value=True)
    if enable_selection:
        st.sidebar.subheader("Selection options")
        selection_mode = st.sidebar.radio("Selection Mode", ['single','multiple'], index=1)

        use_checkbox = st.sidebar.checkbox("Use check box for selection", value=True)
        if use_checkbox:
            groupSelectsChildren = st.sidebar.checkbox("Group checkbox select children", value=True)
            groupSelectsFiltered = st.sidebar.checkbox("Group checkbox includes filtered", value=True)

        if ((selection_mode == 'multiple') & (not use_checkbox)):
            rowMultiSelectWithClick = st.sidebar.checkbox("Multiselect with click (instead of holding CTRL)", value=False)
            if not rowMultiSelectWithClick:
                suppressRowDeselection = st.sidebar.checkbox("Suppress deselection (while holding CTRL)", value=False)
            else:
                suppressRowDeselection=False
        st.sidebar.text("___")

    enable_pagination = st.sidebar.checkbox("Enable pagination", value=False)
    if enable_pagination:
        st.sidebar.subheader("Pagination options")
        paginationAutoSize = st.sidebar.checkbox("Auto pagination size", value=True)
        if not paginationAutoSize:
            paginationPageSize = st.sidebar.number_input("Page size", value=5, min_value=0, max_value=sample_size)
        st.sidebar.text("___")

    df = fetch_data(sample_size)

    #Infer basic colDefs from dataframe types
    gb = GridOptionsBuilder.from_dataframe(df)

    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gb.configure_column("date_only", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd', pivot=True)
    gb.configure_column("date_tz_aware", type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

    gb.configure_column("apple", type=["numericColumn","numberColumnFilter","customNumericFormat"], precision=2, aggFunc='sum')
    gb.configure_column("banana", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=1, aggFunc='avg')
    gb.configure_column("chocolate", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='max')

    #configures last row to use custom styles based on cell's value, injecting JsCode on components front end
    cellsytle_jscode = JsCode("""
    function(params) {
        if (params.value == 'A') {
            return {
                'color': 'white',
                'backgroundColor': 'darkred'
            }
        } else {
            return {
                'color': 'black',
                'backgroundColor': 'white'
            }
        }
    };
    """)
    gb.configure_column("group", cellStyle=cellsytle_jscode)

    if enable_sidebar:
        gb.configure_side_bar()

    if enable_selection:
        gb.configure_selection(selection_mode)
        if use_checkbox:
            gb.configure_selection(selection_mode, use_checkbox=True, groupSelectsChildren=groupSelectsChildren, groupSelectsFiltered=groupSelectsFiltered)
        if ((selection_mode == 'multiple') & (not use_checkbox)):
            gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=rowMultiSelectWithClick, suppressRowDeselection=suppressRowDeselection)

    if enable_pagination:
        if paginationAutoSize:
            gb.configure_pagination(paginationAutoPageSize=True)
        else:
            gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=paginationPageSize)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    #Display the grid
    st.header("Streamlit Ag-Grid")
    st.markdown("""
        AgGrid can handle many types of columns and will try to render the most human readable way.  
        On editions, grid will fallback to string representation of data, DateTime and TimeDeltas are converted to ISO format.
        Custom display formating may be applied to numeric fields, but returned data will still be numeric.
    """)

    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        height=grid_height, 
        width='100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        enable_enterprise_modules=enable_enterprise_modules
        )

    df = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')


    with st.spinner("Displaying results..."):
        #displays the chart
        chart_data = df.loc[:,['apple','banana','chocolate']].assign(source='total')

        if not selected_df.empty :
            selected_data = selected_df.loc[:,['apple','banana','chocolate']].assign(source='selection')
            chart_data = pd.concat([chart_data, selected_data])

        chart_data = pd.melt(chart_data, id_vars=['source'], var_name="item", value_name="quantity")
        #st.dataframe(chart_data)
        chart = alt.Chart(data=chart_data).mark_bar().encode(
            x=alt.X("item:O"),
            y=alt.Y("sum(quantity):Q", stack=False),
            color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
        )

        st.header("Component Outputs - Example chart")
        st.markdown("""
        This chart is built with data returned from the grid. rows that are selected are also identified.
        Experiment selecting rows, group and filtering and check how the chart updates to match.
        """)

        st.altair_chart(chart, use_container_width=True)

        st.subheader("Returned grid data:") 
        #returning as HTML table bc streamlit has issues when rendering dataframes with timedeltas:
        # https://github.com/streamlit/streamlit/issues/3781
        st.markdown(grid_response['data'].to_html(), unsafe_allow_html=True)

        st.subheader("grid selection:")
        st.write(grid_response['selected_rows'])

        st.header("Generated gridOptions")
        st.markdown("""
            All grid configuration is done thorugh a dictionary passed as ```gridOptions``` parameter to AgGrid call.
            You can build it yourself, or use ```gridOptionBuilder``` helper class.  
            Ag-Grid documentation can be read [here](https://www.ag-grid.com/documentation)
        """)
        st.write(gridOptions)
        '''