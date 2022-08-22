import streamlit as st
from Logout import db, auth

query = db.child('itens').get().val().values()

df_itens = pd.DataFrame()
for i in query:
    df_itens = pd.concat([df_itens, pd.DataFrame({x:[i[x]] for x in i})],ignore_index=True)

st.title('Emitir Relatório')

st.dataframe(df_itens)