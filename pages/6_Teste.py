import json
import streamlit as st
import pandas as pd
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from Logout import db, auth
from utilidades import nav_page
from streamlit_gallery.components.elements.dashboard import Dashboard, Editor, Card, DataGrid, Radar, Pie, Player

st.set_page_config(layout="wide")

if st.session_state['authentication_status'] != True or 'authentication_status' not in st.session_state:
    nav_page('')
else:

    query = list(db.child('itens').order_by_child('situacao').equal_to('cadastrado').get().val().values())


    def main():

        if "w" not in state:
            board = Dashboard()
            w = SimpleNamespace(
                dashboard=board,
                editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
                player=Player(board, 0, 12, 6, 10, minH=5),
                pie=Pie(board, 6, 0, 6, 7, minW=3, minH=4),
                radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
                card=Card(board, 6, 7, 3, 7, minW=2, minH=4),
                data_grid=DataGrid(board, 6, 13, 6, 7, minH=4),
            )
            state.w = w

            w.editor.add_tab("Card content", Card.DEFAULT_CONTENT, "plaintext")
            w.editor.add_tab("Itens cadastrados", json.dumps(query), "json")
            w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")
            w.editor.add_tab("Pie chart", json.dumps(Pie.DEFAULT_DATA, indent=2), "json")
        else:
            w = state.w

        with elements("demo"):
            event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

            with w.dashboard(rowHeight=57):
                #w.editor()
                #w.player()
                #w.pie(w.editor.get_content("Pie chart"))
                #w.radar(w.editor.get_content("Radar chart"))
                #w.card(w.editor.get_content("Card content"))
                w.data_grid(w.editor.get_content("Itens cadastrados"))

    main()

    '''    
    df_final = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected)

    st.write(df_itens)
    st.write(df_final)
    st.write(selected)
    st.write(selected_df)'''

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