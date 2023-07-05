###########################################################################################
#### UM GRUPO DE CODIGOS NECESSITA DE MELHORIAS EM SUAS LOGICAS POR POSSIVEIS FALACIAS ####
####    OU SEJA ALGUNS DESSES CODIGOS FALAM A MESMA COISA DUAS OU MAIS VEZES           ####
#### O SISTEMA DO STREAMLIT POSSUI ALGUMAS LIMITAÇÕES, A PRINCIPAL FRUSTAÇÃO ENCONTRADA####
#### É O FATO DA FERRAMENTAapresentarFALTA DE "REAÇÃO" OU DEMORA DESTA, SE VC BUSCA    ####
####        POR ALGO QUE RESOLVA ISSO, ACESSE https://youtu.be/QiiwEAz6BVY             ####
####                        BOA SORTE E TENTE NÃO ENLOUQUECER                          ####
###########################################################################################


import streamlit as st
import numpy as np
import pandas as pd
import datetime as DT
import math
import time as tm
from func.redirect import nav_page

from msal_streamlit_authentication import msal_authentication


st.set_page_config(
    page_icon="invest_smart_logo.png",
    page_title="Simulador 0.55",
    initial_sidebar_state="collapsed",
    # layout="wide"
)

st.title('Página de Login')

text,botao =st.columns(2)

with botao:

    login_token = msal_authentication(
        auth={
            "clientId": st.secrets.masl_clientid,
            "authority": st.secrets.msal_authority,
            "redirectUri": st.secrets.msal_redirect,
            "postLogoutRedirectUri": st.secrets.msal_post
        }, # Corresponds to the 'auth' configuration for an MSAL Instance
        cache={
            "cacheLocation": "sessionStorage",
            "storeAuthStateInCookie": True
        } # Corresponds to the 'cache' configuration for an MSAL Instance
    )


with text:
    if login_token ==None:
        st.write('')
        st.write('')
        # st.write('')
        # st.write('')
        st.write(
        fr'<p style="font-size:26px;">Por favor clique no botão ao lado, para entrar na ferramenta com seu email da empresa</p>',
        unsafe_allow_html=True,
    )
        #st.write("Por favor clique no botão ao lado, para entrar na ferramenta com seu email da empresa")
        st.stop()
    else:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        value=login_token['account']['name']
        st.write(
        f'<p style="font-size:26px;">Bem Vindo/a,{value}</p>',
        unsafe_allow_html=True,
    )
        #st.subheader(f"BEM VINDO/A, {login_token['account']['name']}")

nome=login_token['account']['name']
username=login_token['account']['username']


st.session_state["usuario"] = username
st.session_state["assessor"] = nome
st.session_state["logout"] = login_token

st.write(f"Você está Utilizando o Email, {username}")

st.write('')
st.write('')


if st.button("Iniciar a ferramenta"):
    nav_page("wide_project")

no_sidebar_style = """
    <style>
        div [data-testid="stToolbar"] {display: none;}
        #MainMenu {visibility: hidden;}
        div[data-testid="stSidebarNav"] {display: none;}
        footer {visibility: hidden;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)


with open(r'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
