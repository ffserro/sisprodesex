import streamlit as st
from streamlit_app import auth
from utilidades import nav_page
import pandas as pd
import numpy as np


st.set_page_config(page_title='SISPRODESEX', page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items=None)
if auth.current_user == None:
    nav_page('main')
else:
    st.markdown("# Seja bem vindo ao PRODESEX")
    st.sidebar.markdown("# Página principal")
    

























    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text('Loading data...')
    data = load_data(10000)
    data_load_state.text("Done! (using st.cache)")
    
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    st.subheader('Quantidades de viagens por hora')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
    st.bar_chart(hist_values)

    hour_to_filter = st.slider('hour', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
    st.subheader(f'Mapa das viagens que iniciaram às {hour_to_filter}:00')
    st.map(filtered_data)
