import streamlit as st
from Logout import db, auth
import pandas as pd
from datetime import datetime

query = db.child('itens').get().val().values()

df_itens = pd.DataFrame()
for i in query:
    df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)

st.title('Emitir Relatório')

st.dataframe(df_itens)

st.download_button('Baixar relatório', df_itens.to_excel(f'Relatorio{datetime.now().year}{datetime.now().month}{datetime.now().day), f'Relatorio{datetime.now().year}{datetime.now().month}{datetime.now().day}.xls')