import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_elements import elements, mui, html, dashboard
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

with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 2, 2),
        dashboard.Item("second_item", 2, 0, 2, 2, isDraggable=False, moved=False),
        dashboard.Item("third_item", 0, 2, 1, 1, isResizable=False),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item")

    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item")