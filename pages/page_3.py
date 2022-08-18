from utilidades import nav_page
try:
    if session_state['authentication_status'] == True:
        st.markdown("# Página 3")
        st.sidebar.markdown("# Página 3")
except:
    nav_page('streamlit_app')