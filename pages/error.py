import streamlit as st
from func.redirect import nav_page

st.set_page_config(
        page_icon="invest_smart_logo.png",
        page_title="Simulador - error",
        initial_sidebar_state="collapsed",
        layout="wide",
    )

col1, mid, col2 = st.columns([20, 2, 5])
with col1:
    st.write(
        fr'<p style="font-size:26px;">HOUVE UM PROBLEMA, ACESSOR</p>',
        unsafe_allow_html=True,
    )

with col2:
    st.image("investsmart_endosso_horizontal_fundopreto.png", width=270)
    
    

if st.button('Logout',key='logout123'):
    nav_page('')

st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)
st.error('Houve um erro durante a execução do programa, por favor clique no botão de logout e tente novamente')

st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)

with open(r'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)