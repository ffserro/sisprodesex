import streamlit as st
import pandas as pd
import numpy as np


st.markdown("# Page 2")
st.sidebar.markdown("# Page 2")

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')
@st.cache
def load_data(nrows):
  data = pd.read_csv(DATA_URL, nrows=nrows)
  lowercase = lambda x: str(x).lower()
  data.rename(lowercase, axis='columns', inplace=True)
  data[DATE_COLUMN]=pd.to_date_time(data[DATE_COLUMN])
  return data

data_load_state = st.text('Carregando os dados...')
data = load_data(10000)
data_load_state.text('Concluído! (using st.cache)')

