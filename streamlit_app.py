import streamlit as st
import numpy as np
import pandas as pd

st.title('Página teste do Rosalvito')

dor = st.slidebar('Quanta dor você está sentindo hoje?',0,100)