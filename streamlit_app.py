from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import time

st.markdown("# Main page")
st.sidebar.markdown("# Main page")
st.title("Aplicativo Teste")
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
"""
with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
"""
df = pd.DataFrame({
    'first column':[1,2,3,4],
    'second column':[10,20,30,40]
})
df

st.write("Teste de planilha:")
st.table(df)

dataframe = pd.DataFrame(np.random.randn(10,20),
columns = ('col %d'%i for i in range(20)))
st.dataframe(dataframe.style.highlight_max(axis=0))

st.table(dataframe)

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns = ['a','b','c'])
st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000,2) / [50,50] + [37.76,-122.4],
    columns = ['lat','lon'])
st.map(map_data)

x = st.slider('x')
st.write(x, 'squared is', x**2)

st.text_input('Your name', key='name')
st.session_state.name

if st.checkbox('Show dataframe'):
    st.line_chart(chart_data)

option = st.selectbox(
    'Esolha um número: ',
    df['first column'])
'Você selecionou: ', option

add_selectbox = st.sidebar.selectbox(
    'Como você gostaria de ser contatado?',
    ('Email', 'Telefone', 'Celular'))
add_slider = st.sidebar.slider(
    'Escolha uma faixa de valores:',
    0.0,100.0,(25.0,75.0))

left_column, right_column = st.columns(2)
left_column.button('Clique aqui!')
with right_column:
    chosen = st.radio(
        'Chapéu seletor',
        ('Grifinória', 'Corvinal', 'Lufa-Lufa', 'Sonserina'))
    st.write(f'Você está na casa {chosen}!')

'Começando uma longa computação...'
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i+1)
    time.sleep(0.1)
"...and now we're done!"
