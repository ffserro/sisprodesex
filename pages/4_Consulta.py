import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_app import db
df_itens = pd.DataFrame(columns=['pi', 'nome', 'descricao', 'lvad', 'data_envio', 'preco_unitario', 'quantidade', 'situacao', 'uf'])
query = db.child('itens').order_by_child('situacao').equal_to('cadastrado').get().val().values()
for i in query:
	df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)
st.write(df_itens)

_selectable_data_table = components.declare_component(
    "selectable_data_table", url="http://localhost:3001")

def selectable_data_table(data, key=None):
    return _selectable_data_table(data=data, default=[], key=key)

rows = selectable_data_table(df_itens)
if rows:
    st.write("You have selected", rows)