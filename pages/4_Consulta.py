import json
from types import SimpleNamespace
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_elements import elements, mui, html, dashboard
from streamlit_app import db
from dashboard.dashboard import dashboard, editor


df_itens = pd.DataFrame(columns=['pi', 'nome', 'descricao', 'lvad', 'data_envio', 'preco_unitario', 'quantidade', 'situacao', 'uf'])
query = db.child('itens').order_by_child('situacao').equal_to('cadastrado').get().val().values()
for i in query:
	df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)
st.write(df_itens)







if 'w' not in st.session_state:
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
    st.session_state.w = w

    w.editor.add_tab('Data Grid', json.dumps(query, ident=2), "json")

else:
    w = st.session_state.w

with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)

        with w.dashboard(rowHeight=57):
            w.data_grid(w.editor.get_content("Data grid"))