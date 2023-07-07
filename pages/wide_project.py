import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import datetime as DT
import math
import time as tm
from func.redirect import nav_page
from st_aggrid import JsCode, AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
from st_aggrid.shared import GridUpdateMode, AgGridTheme
from database import base_df, besmart_base, moeda, PositivadorBitrix
import locale
from msal_streamlit_authentication import msal_authentication
import requests

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

if 'usuario' not in st.session_state:
    nav_page('error')

st.set_page_config(
    page_icon="invest_smart_logo.png",
    page_title="Simulador - Clientes 0.55",
    initial_sidebar_state="collapsed",
    layout="wide",
)

#df = pd.read_sql("SELECT * FROM cliente", con)
courier= int(st.secrets.courier)
df = PositivadorBitrix().get_all_data_cliente(courier)
df = df.rename(columns={st.secrets.id:'client_id',st.secrets.VAR_SIGLA_ASSESSOR:'sigla',st.secrets.VAR_NOME_CLIENTE:'nome_client',st.secrets.VAR_DATA_ENTRADA_CLIENTE:'data_cliente'})

dark = df.copy()
dark = dark.rename(
    columns={
        "nome_client": "Nome do Cliente",
        "data_cliente": "Data de Cadastro",
    }
)

id_v1 = st.session_state.usuario

#st.dataframe(df)
dark = dark[dark["sigla"] == id_v1]



if dark.empty:
    dark = pd.DataFrame(
        columns={
            "client_id",
            "sigla",
            "Nome do Cliente",
            "Data de Cadastro",
            "Qnt. Ativos InvestSmart",
            "Qnt. Produtos BeSmart",
            "PL Aplicado",
        }
    ).fillna(0)

# st.dataframe(dark)
# dark[pl] = st.session_state.df_cliente.client_id[0]
#st.write(st.session_state.usuario)
col1, mid, col2 = st.columns([20, 2, 5])
with col1:
    st.markdown(
        fr'''
        <style>
        @font-face {{
            font-family: 'Knockout';
            src: url('Fonte/Knockout-Bold.ttf') format('truetype'),
            url('Fonte/Knockout-Bold.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
        }}
        </style>
        
        <p style='font-size:26px; font-family: "Knockout"'>Bem Vindo ao Simulador, {st.session_state.assessor}</p>
        ''',
        unsafe_allow_html=True
    )
with col2:
    st.image("investsmart_endosso_horizontal_fundopreto.png", width=270)
    esquerda, direita  = st.columns([5, 4])
    with direita:
        if st.button('Logout',key='logout1'):
            st.session_state["logout"] =None
            if st.session_state["logout"]==None:
                nav_page('')

st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)

#######################################################################################
################################# LAYOUT DO CONTEÚDO ##################################
#######################################################################################
vazio_nulo ,pl, retorno, ano1_avg, ano2_avg  = st.columns([1,5, 5, 5, 3])


st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)
st.write(
        fr'<p style="font-size:26px;">Repasses de Comissão</p>',
        unsafe_allow_html=True,
    )

df_reps = PositivadorBitrix().get_repasse_v2(st.session_state["usuario"])
df_reps = df_reps.rename(columns={
    st.secrets.VAR_ID_EMAIL:'id_email',
    st.secrets.VAR_REPASSE_INVESTSMART:'repasse_investsmart',
    st.secrets.VAR_REPASSE_SEGUROS:'repasse_seguros',
    st.secrets.VAR_REPASSE_CAMBIO:'repasse_cambio',
    st.secrets.VAR_REPASSE_CREDITO:'repasse_credito',
    st.secrets.VAR_REPASSE_IMOVEL:'repasse_imovel',
    st.secrets.id:'repasse_id',
    })
#st.dataframe(df_reps)

space,reps1, reps2, reps3, reps4, reps5, space2 = st.columns( [5,3 ,3 ,3 ,3 ,3, 5] )

space3,salve,space4=st.columns( [5,1,5] )
st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)
vacuo, botao_1, botao_2, botao_3, vacuo_2 = st.columns([9, 3, 3, 3, 9])


vazio1, cliente, vazio2 = st.columns([0.1, 15, 0.1])

st.markdown(
    """
    <hr style="height:1px;border:none;color:#9966ff;background-color:#9966ff;" /> 
    """,
    unsafe_allow_html=True,
)
space5,choice,space6= st.columns([6,5,5])
container = st.container()
chart1, chart2 = st.columns([6, 4])

#######################################################################################
############################ PARTE DO REPASSE ############################
#######################################################################################

try:
    repasse_invest=df_reps['repasse_investsmart'].iloc[0]
    repasse_seguro=df_reps['repasse_seguros'].iloc[0]
    repasse_cambio=df_reps['repasse_cambio'].iloc[0]
    repasse_credito=df_reps['repasse_credito'].iloc[0]
    repasse_imovel=df_reps['repasse_imovel'].iloc[0]
    repasse_id = df_reps['repasse_id'].iloc[0]
    with reps1:
        reps_investsmart=st.number_input('(%) Repasse da InvestSmart',value=int(repasse_invest),min_value=0,max_value=100)
    with reps2:
        reps_seguro=st.number_input('(%) Repasse de Seguros',value=int(repasse_seguro),min_value=0,max_value=100)
    with reps3:
        reps_cambio=st.number_input('(%) Repasse de Câmbio',value=int(repasse_cambio),min_value=0,max_value=100)
    with reps4:
        reps_credito=st.number_input('(%) Repasse de Crédito',value=int(repasse_credito),min_value=0,max_value=100)
    with reps5:
        reps_imovel=st.number_input('(%) Repasse de Imóveis',value=int(repasse_imovel),min_value=0,max_value=100) 
except:    
    with reps1:
        reps_investsmart=st.number_input('(%) Repasse da InvestSmart',value=50,min_value=0,max_value=100)
    with reps2:
        reps_seguro=st.number_input('(%) Repasse de Seguros',value=50,min_value=0,max_value=100)
    with reps3:
        reps_cambio=st.number_input('(%) Repasse de Câmbio',value=50,min_value=0,max_value=100)
    with reps4:
        reps_credito=st.number_input('(%) Repasse de Crédito',value=50,min_value=0,max_value=100)
    with reps5:
        reps_imovel=st.number_input('(%) Repasse de Imóveis',value=50,min_value=0,max_value=100)
#st.write(repasse_id)

st.session_state['reps_investsmart']=reps_investsmart
st.session_state['reps_seguro']=reps_seguro
st.session_state['reps_cambio']=reps_cambio
st.session_state['reps_credito']=reps_credito
st.session_state['reps_imovel']=reps_imovel

with salve:
    if st.button('Salvar valores'):
        if df_reps.empty:
            upgrade=False
        else:
            upgrade=True
        if upgrade:
            url = st.secrets.url_update+f"id={repasse_id}&fields["+st.secrets.VAR16+f"]={st.session_state.reps_investsmart}&fields["+st.secrets.VAR17+f"]={st.session_state.reps_seguro}&fields["+st.secrets.VAR18+f"]={st.session_state.reps_cambio}&fields["+st.secrets.VAR19+f"]={st.session_state.reps_credito}&fields["+st.secrets.VAR20+f"]={st.session_state.reps_imovel}&fields["+st.secrets.category+"]="+st.secrets.bigby
            payload = {}
            headers = {
            'Cookie': 'BITRIX_SM_SALE_UID=0; qmb=0.'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            st.success("O cliente foi adicionado ao banco de dados")
            
            st._rerun()
    
        else:
            url = st.secrets.url_add+"fields["+st.secrets.VAR15+f"]={st.session_state.usuario}&fields["+st.secrets.VAR16+f"]={st.session_state.reps_investsmart}&fields["+st.secrets.VAR17+f"]={st.session_state.reps_seguro}&fields["+st.secrets.VAR18+f"]={st.session_state.reps_cambio}&fields["+st.secrets.VAR19+f"]={st.session_state.reps_credito}&fields["+st.secrets.VAR20+f"]={st.session_state.reps_imovel}&fields["+st.secrets.category+"]="+st.secrets.bigby
            payload = {}
            headers = {
            'Cookie': 'BITRIX_SM_SALE_UID=0; qmb=0.'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            st.success("O cliente foi adicionado ao banco de dados")
            
            st._rerun()
            


#######################################################################################
############################ METRICS USADAS NOS BIGNUMBERS ############################
#######################################################################################



list_client_id = dark["client_id"].unique().astype(int)
list_client_id = list(list_client_id)

#fair = pd.read_sql("SELECT * FROM variaveis", con)
# arabian= int(st.secrets.arabian)
# lista2=list(PositivadorBitrix().get_data_default(arabian)["ID"])

fair = PositivadorBitrix().get_produto_v2()
#fair = fair.dropna(axis=0,thresh=12)
fair = fair.rename(columns={
    st.secrets.VAR_ID_CLIENTE:'client_id',
    st.secrets.VAR_EMPRESA:'empresa',
    st.secrets.VAR_CATEGORIA:'categoria',
    st.secrets.VAR_ATIVO:'ativo',
    st.secrets.VAR_PL_APLICADO:'pl_aplicado',
    st.secrets.VAR_RETORNO:'retorno',
    st.secrets.VAR_REPASSE:'repasse',
    st.secrets.VAR_ROA_HEAD:'roa_head',
    st.secrets.VAR_ROA_REC:'roa_rec',
    st.secrets.VAR_DATA_ATIVO:'data_ativo',
    st.secrets.VAR_DATA_VENC:'data_venc',
    st.secrets.id:'ativo_id',
    })
#st.dataframe(lista2)
fair=fair[fair['client_id'].isin(dark['client_id'].astype(str))]
fair['pl_aplicado']= fair['pl_aplicado'].astype(float)
fair['pl_aplicado']= fair['pl_aplicado'].astype(int)
fair['client_id']= fair['client_id'].astype(int)
#st.dataframe(fair)
fair['retorno']= fair['retorno'].astype(float)
fair['repasse']= fair['repasse'].astype(float)
fair['roa_head']= fair['roa_head'].astype(float)
fair['roa_rec']= fair['roa_rec'].astype(float)
fair['ativo_id']= fair['ativo_id'].astype(int)
fair = fair[fair.client_id.isin(list_client_id)]

#st.dataframe(fair)
dicio = fair.groupby("client_id")["pl_aplicado"].sum()
dark["PL Aplicado"] = (
    df["client_id"]
    .map(dicio)
    .apply(lambda x: locale.currency(x, grouping=True, symbol=True))
)
#st.dataframe(dark)
dark["PL Aplicado"] = dark["PL Aplicado"].replace("R$ nan", "R$ 0,00")

dark["Investimentos"] = (
    df["client_id"]
    .map(fair[fair.empresa=='INVESTSMART'].groupby("client_id")["pl_aplicado"].sum())
    .apply(lambda x: locale.currency(x, grouping=True, symbol=True))
)
dark["Investimentos"] = dark["Investimentos"].replace("R$ nan", "R$ 0,00")

fair["karma"] = [
    "InvestSmart" if x == "INVESTSMART" else "BeSmart" for x in fair["empresa"]
]
#st.dataframe(fair)
pl.metric(
    "Total do Portifólio",
    "R$ " + locale.currency(fair[fair.empresa=='INVESTSMART'].pl_aplicado.sum(), grouping=True, symbol=None)[:-3],
)

if fair.pl_aplicado.sum() == 0:
    dark["Qnt. Ativos InvestSmart"] = 0
    dark["Qnt. Produtos BeSmart"] = 0
    dark["PL Aplicado"] = 0

else:
    try:
        dark["Qnt. Ativos InvestSmart"] = [
            fair[fair["client_id"] == x].value_counts("karma")["InvestSmart"]
            if x in fair["client_id"].unique()
            else 0
            for x in dark["client_id"].unique()
        ]
        dark["Qnt. Produtos BeSmart"] = [
            fair[fair["client_id"] == x]
            .value_counts("karma")
            .reindex(fair.karma.unique(), fill_value=0)
            .sum()
            - fair[fair["client_id"] == x]
            .value_counts("karma")
            .reindex(fair.karma.unique(), fill_value=0)["InvestSmart"]
            if x in fair["client_id"].unique()
            else 0
            for x in dark["client_id"].unique()
        ]
    except:
        dark["Qnt. Produtos BeSmart"] = [
            fair[fair["client_id"] == x].value_counts("karma").reindex(fair.karma.unique(), fill_value=0)["BeSmart"]
            if x in fair["client_id"].unique()
            else 0
            for x in dark["client_id"].unique()
        ]

        dark["Qnt. Ativos InvestSmart"] = [
            fair[fair["client_id"] == x]
            .value_counts("karma")
            .reindex(fair.karma.unique(), fill_value=0)
            .sum()
            - fair[fair["client_id"] == x]
            .value_counts("karma")
            .reindex(fair.karma.unique(), fill_value=0)["BeSmart"]
            if x in fair["client_id"].unique()
            else 0
            for x in dark["client_id"].unique()
        ]



smart = pd.DataFrame(columns=["Mês", "Resultado assessor",'Faturamento','Resultado Bruto'])


face = pd.read_excel("base_besmart_v3.xlsx")
face["Categoria"] = face["Categoria"].apply(lambda x: x.replace("_", " "))
face["Produto"] = face["Produto"].apply(lambda x: x.replace("_", " "))
face["porcem_repasse"] = face["porcem_repasse"] * 100.0

for i in fair["ativo_id"].unique():
    df = fair[fair["ativo_id"] == i]
    df = df.reset_index().drop('index', axis= 1)

    #st.dataframe(df)
    masquerede = face[
        (face["Empresa"] == "Credito")
        & (face["Categoria"] == 'Colaterizado')
        & (face["Produto"] == "Crédito XP")]
    #st.dataframe(masquerede)
    if df.empresa.iloc[0] == "INVESTSMART":
        grasph_df = base_df(
            df.data_venc.iloc[0],
            df.data_ativo.iloc[0],
            df.pl_aplicado.iloc[0],
            df.retorno.iloc[0],
            df.roa_head.iloc[0],
            df.roa_rec.iloc[0],
            st.session_state.reps_investsmart,
            moeda_real=False,
        )
        grasph_df["id"] = df.client_id[0]
    else:
        if df.empresa.iloc[0] == "Seguros":
            repasse = st.session_state.reps_seguro
        elif df.empresa.iloc[0] == "Câmbio":
            repasse = st.session_state.reps_cambio
        elif df.empresa.iloc[0] == "Crédito":
            repasse = st.session_state.reps_credito
        else:
            repasse = st.session_state.reps_imovel
        grasph_df = besmart_base(
            df.data_venc.iloc[0],
            df.data_ativo.iloc[0],
            face,
            df.empresa.iloc[0],
            df.categoria.iloc[0],
            df.ativo.iloc[0],
            df.pl_aplicado.iloc[0],
            repasse,
        )
        grasph_df["id"] = df.client_id[0]
    #st.dataframe(grasph_df)
    smart = smart.append(grasph_df)
smart["Mês"] = smart["Mês"].apply(lambda x: DT.datetime.strptime(x, "%b-%y"))
smart["Mês"] = smart["Mês"].apply(lambda x: DT.datetime.strftime(x, "%m-%y"))
#st.dataframe(smart)
smart['Total Bruto'] = smart['Faturamento'].fillna(0) + smart['Resultado Bruto'].fillna(0)
try:
    Invest = smart[smart['PL Retido'].notna()]
    Invest = (Invest[["Mês", "Resultado assessor","Total Bruto"]]
        .groupby(Invest["Mês"])#["Resultado assessor"]
        .sum()
        .reset_index())
    Invest["Mês"] = Invest["Mês"].apply(lambda x: DT.datetime.strptime(x, "%m-%y"))
    Invest["ano"] = Invest["Mês"].astype("datetime64").dt.year
    Invest["mes"] = Invest["Mês"].astype("datetime64").dt.month
    Invest["Mês"] = Invest["Mês"].apply(lambda x: DT.datetime.strftime(x, "%b-%y"))
    Invest = Invest.sort_values(["ano", "mes"]).reset_index(drop=True)
    Invest["label"]= "InvestSmart"
except:
    Invest = pd.DataFrame(columns={
        "Mês",
        "Resultado assessor",
        "ano",
        "mes",
        "label",
        "Total Bruto"
    })
try:
    Besmart = smart[smart['Custo do Produto'].notna()]
    Besmart = (Besmart[["Mês", "Resultado assessor","Total Bruto"]]
        .groupby(Besmart["Mês"])#["Resultado assessor"]
        .sum()
        .reset_index())
    Besmart["Mês"] = Besmart["Mês"].apply(lambda x: DT.datetime.strptime(x, "%m-%y"))
    Besmart["ano"] = Besmart["Mês"].astype("datetime64").dt.year
    Besmart["mes"] = Besmart["Mês"].astype("datetime64").dt.month
    Besmart["Mês"] = Besmart["Mês"].apply(lambda x: DT.datetime.strftime(x, "%b-%y"))
    Besmart["label"]= "BeSmart"
except:
    Besmart = pd.DataFrame(columns={
        "Mês",
        "Resultado assessor",
        "ano",
        "mes",
        "label",
        "Total Bruto"
    })
try:
    super_smart = Besmart.append(Invest)
    super_smart = super_smart.sort_values(["ano", "mes"]).reset_index(drop=True)

except:
    super_smart = pd.DataFrame(columns={
        "Mês",
        "Resultado assessor",
        "ano",
        "mes",
        "label",
        "Total Bruto"
    })

final = (
    smart[["Mês", "Resultado assessor","Total Bruto"]]
    .groupby(smart["Mês"])#["Resultado assessor"]
    .sum()
    .reset_index()
)


final["Mês"] = final["Mês"].apply(lambda x: DT.datetime.strptime(x, "%m-%y"))
final["ano"] = final["Mês"].astype("datetime64").dt.year
final["mes"] = final["Mês"].astype("datetime64").dt.month
final["Mês"] = final["Mês"].apply(lambda x: DT.datetime.strftime(x, "%b-%y"))
final = final.sort_values(["ano", "mes"]).reset_index(drop=True)
#st.dataframe(final)
try:
    result_month = final["Resultado assessor"][(final["mes"] == DT.datetime.now().month)& (final["ano"] == DT.datetime.now().year)]
    avrg_year1 = (final["Resultado assessor"][final["ano"] == DT.datetime.now().year].sum())
    avrg_year2 = (final["Resultado assessor"][
        final["ano"] == DT.datetime.now().year + 1
    ].sum())
except:
    result_month = 0
    avrg_year1 = 0
    avrg_year2 = 0
try:
    retorno.metric(
        "Comissão Esperada para esse mês",
        "R$ "
        + locale.currency(
            result_month.iloc[0],
            grouping=True,
            symbol=None,
        )[:-3],
    )
except:
    retorno.metric(
        "Comissão Esperada para esse mês",
        "R$ "
        + locale.currency(
            0,
            grouping=True,
            symbol=None,
        )[:-3],
    )

ano1_avg.metric(
    f"Comissão Esperada de {DT.datetime.now().year}",
    "R$ "
    + locale.currency(
        avrg_year1,
        grouping=True,
        symbol=None,
    )[:-3],
)

ano2_avg.metric(
    f"Comissão Esperada de {DT.datetime.now().year+1}",
    "R$ "
    + locale.currency(
        avrg_year2,
        grouping=True,
        symbol=None,
    )[:-3],
)



#######################################################################################
################################ COMISSÃO POR CLIENTE #################################
#######################################################################################
metrics = smart.copy()
metrics["Mês"] = metrics["Mês"].apply(lambda x: DT.datetime.strptime(x, "%m-%y"))
metrics["ano"] = metrics["Mês"].astype("datetime64").dt.year
metrics["mes"] = metrics["Mês"].astype("datetime64").dt.month
metrics["Mês"] = metrics["Mês"].apply(lambda x: DT.datetime.strftime(x, "%b-%y"))
metrics = metrics.sort_values(["ano", "mes"]).reset_index(drop=True)
#st.dataframe(metrics)

dark[f"Comissão esperada {DT.datetime.now().year}"] =[0 if metrics.empty else
    locale.currency(metrics[["ano", "Resultado assessor","id","mes"]][(metrics["ano"] == DT.datetime.now().year) & (metrics["id"] == i)].groupby("mes").sum()["Resultado assessor"].sum(), grouping=True) for i in dark["client_id"]
]

dark[f"Comissão esperada {DT.datetime.now().year+1}"] =[0 if metrics.empty else
locale.currency(metrics[["ano", "Resultado assessor","id","mes"]][(metrics["ano"] == DT.datetime.now().year+1) & (metrics["id"] == i)].groupby("mes").sum()["Resultado assessor"].sum(), grouping=True) for i in dark["client_id"]
]

try:
    dark["Investimentos"] = dark["Investimentos"].apply(lambda x: x[:-3])
except:
    pass
try:
    dark[f"Comissão esperada {DT.datetime.now().year}"] = dark[f"Comissão esperada {DT.datetime.now().year}"].apply(lambda x: x[:-3])
except:
    dark[f"Comissão esperada {DT.datetime.now().year}"] = 0
try:
    dark[f"Comissão esperada {DT.datetime.now().year+1}"] = dark[f"Comissão esperada {DT.datetime.now().year+1}"].apply(lambda x: x[:-3])
except:
    
    dark[f"Comissão esperada {DT.datetime.now().year+1}"] = 0

#st.dataframe(dark)
# st.dataframe(result_month)
dark = dark.replace("R$ nan", "R$ 0")



#######################################################################################
############################### TABLES CLIENTE E ATIVOS ###############################
#######################################################################################

with cliente:
    # dark["PL Aplicado"] = dark["PL Aplicado"].apply(lambda x: "R$ " + str(x))
    htmlstr = f'''<p style='background-color: #9966ff;  font-family: "Knockout"; color: #000000; font-size: 20px; border-radius: 7px; padding-left: 8px; text-align: center'>Carteira de Clientes</style></p>'''
    st.markdown(htmlstr, unsafe_allow_html=True)

    gridOptions = GridOptionsBuilder.from_dataframe(
        dark[
            [
                "Nome do Cliente",
                "Data de Cadastro",
                "Investimentos",
                "Qnt. Ativos InvestSmart",
                "Qnt. Produtos BeSmart",
                f"Comissão esperada {DT.datetime.now().year}",
                f"Comissão esperada {DT.datetime.now().year+1}"
            ]
        ]
    )

    gridOptions.configure_selection(
        selection_mode="single", use_checkbox=True, pre_selected_rows=[0]
    )
    gb = gridOptions.build()

    custom_css = {
        ".ag-theme-alpine": {
            "--ag-background-color": "#fff !important",
            "--ag-foreground-color": "#181d1f !important",
            "--ag-subheader-background-color": "#fff !important",
            "--ag-alpine-active-color": "#EBFF70 !important",
            "--ag-range-selection-border-color": "#EBFF70 !important",
            "font-family": ' "Barlow" !important'
        }
    } 

    dta = AgGrid(
        dark,
        gridOptions=gb,
        #height=290,
        allow_unsafe_jscode=True,
        theme=AgGridTheme.ALPINE,
        fit_columns_on_grid_load =True,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
        reload_data=True,
        custom_css=custom_css
    )
    @st.cache_data

    def convert_df(df):
     df = df[["Nome do Cliente","Data de Cadastro","Investimentos","Qnt. Ativos InvestSmart","Qnt. Produtos BeSmart",f"Comissão esperada {DT.datetime.now().year}",f"Comissão esperada {DT.datetime.now().year+1}"]]
    
     return df.to_csv(sep = ';', index=False).encode('utf-8-sig')
    
    csv = convert_df(dta["data"])

    st.download_button(
    label="Download",
    data=csv,
    file_name='clientes.csv',
    mime='text/csv',)

st.session_state["df_cliente"] = pd.DataFrame(dta["selected_rows"])

if st.session_state["df_cliente"].empty:
    table2 = fair.copy()
else:
    table2 = fair[fair["client_id"] == st.session_state["df_cliente"].client_id.iloc[0]]


table2 = table2.rename(
    columns={
        "categoria": "Categoria",
        "ativo": "Ativo",
        "pl_aplicado": "PL Aplicado",
        "data_venc": "Data de Vencimento",
        "data_ativo": "Data de Início",
        "empresa": "Empresa",
    }
)

today = DT.datetime.strftime(DT.datetime.today(), "%Y-%m-%d")
hoje = today

with botao_1:
    if "button1" not in st.session_state:
        st.session_state["button1"] = False

    if st.button("Cadastrar um Cliente"):
        st.session_state["button1"] = not st.session_state["button1"]

    if st.session_state["button1"]:
        disco = st.text_input("Nome do Cliente: ", value="")
        if st.button("Salvar"):
            
            url = st.secrets.url_add+"fields["+st.secrets.VAR1+f"]={id_v1}&fields["+st.secrets.VAR2+f"]={disco}&fields["+st.secrets.VAR3+f"]={today}&fields["+st.secrets.category+"]="+st.secrets.courier
            payload = {}
            headers = {
            'Cookie': 'BITRIX_SM_SALE_UID=0; qmb=0.'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            st.success("O cliente foi adicionado ao banco de dados")
            
            st._rerun()
#st.dataframe(st.session_state.df_cliente)
#st.write("https://"+st.secrets.domain+"rest/"+st.secrets.bignumber+"/"+st.secrets.cod_shhh+"/crm.deal.delete?["+st.secrets.id+f"]={st.session_state.df_cliente.client_id.iloc[0]}")
with botao_3:
    if "button42" not in st.session_state:
        st.session_state["button42"] = False

    if st.button("Deletar um Portifólio"):
        st.session_state["button42"] = not st.session_state["button42"]

    if st.session_state["button42"]:
        disco = st.write("Tem Certeza ?")
        sim, nao = st.columns(2)
        with sim:
            if st.button("Sim"):
                if (
                    st.session_state["df_cliente"].empty
                    or dta.data["Data de Cadastro"].iloc[0] == "None"
                ):
                    st.error("Não foi selecionado um Cliente")
                else:
                    with st.spinner("Aguarde"):
                        list_id_del= fair[fair["client_id"]==st.session_state.df_cliente.client_id.iloc[0]]['ativo_id']
                        for a in list_id_del:
                            url = st.secrets.url_delete+'id'+f"={a}"
                            payload = {}
                            headers = {
                            'Cookie': 'BITRIX_SM_SALE_UID=30; qmb=0.'
                            }
                            response = requests.request("POST", url, headers=headers, data=payload)
                        
                        vers = st.session_state.df_cliente.client_id.iloc[0]
                        url = st.secrets.url_delete+'id'+f"={vers}"
                        payload = {}
                        headers = {
                        'Cookie': 'BITRIX_SM_SALE_UID=30; qmb=0.'
                        }
                        response = requests.request("POST", url, headers=headers, data=payload)
                        #print(response.text)
                    st.success("O cliente foi deletado com sucesso")
                    st._rerun()
        with nao:
            if st.button("Não"):
                st.session_state["button42"] = False

with botao_2:
    if st.button("Visualizar o Portifólio"):
        if (
            st.session_state["df_cliente"].empty
            or dta.data["Data de Cadastro"].iloc[0] == "None"
        ):
            st.error("Não foi selecionado um Cliente")
        else:
            nav_page("cliente_wide")

#st.write(int(st.session_state.df_cliente.client_id.iloc[0]))




#######################################################################################
################################### GRAFICOS FEITOS ###################################
#######################################################################################



with open(r'style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#st.dataframe(super_smart)
# chart1, chart2 = st.columns([6, 4])
if super_smart.empty:
    st.text("")
    st.error("Assessor não tem Portifólio")
else:    
    super_smart["data"] = super_smart["Mês"].apply(lambda x: DT.datetime.strptime(x,"%b-%y"))
    super_smart["data"] = super_smart["data"].apply(lambda x: DT.datetime.strftime(x, "%Y/%m"))
    #st.dataframe(super_smart["data"].unique())

    distancia = list(super_smart["data"].unique())
    distancia_df = pd.DataFrame(distancia)
    #st.dataframe(distancia_df)
    distancia_df["ano"] = distancia_df[0].astype("datetime64").dt.year
    #st.dataframe(super_smart)
    #super_smart['Total Bruto'] = super_smart['Faturamento'].fillna(0) + super_smart['Resultado Bruto'].fillna(0)
    with choice:
        coluna = st.radio("Qual tipo de Gráfico é desejado ?",["Comissão Líquida - Assessor","Resultado Bruto"],horizontal=True,key='uno_first')
        if coluna == "Comissão Líquida - Assessor":
            subst = "Resultado assessor"
        else:
            subst = "Total Bruto"
    with container:
        try:
            i_n_v = distancia_df[distancia_df["ano"] == DT.datetime.now().year + 2].reset_index().iloc[-1]["index"]
            inc, end = st.select_slider("Período de tempo do Grafico",options = distancia,value=(distancia[0],distancia[i_n_v]))
        except:
            inc, end = st.select_slider("Período de tempo do Grafico",options = distancia,value=(distancia[0],distancia[-1]))

    with chart2:
        try:
            #st.dataframe(fair)
            df_categ = fair[fair["empresa"]=="INVESTSMART"].groupby("categoria")["pl_aplicado"].sum().reset_index()
            df_categ['label'] = df_categ["pl_aplicado"].apply(lambda x: locale.currency(x, grouping=True)[:-3])
            df_categ = df_categ.sort_values(by="pl_aplicado", ascending=False)
            #st.dataframe(df_categ)
            fig = px.bar(
                df_categ,
                x="pl_aplicado",
                y="categoria",
                #width=700,
                height=600,
                text=df_categ.label,
                color="categoria",
                color_discrete_sequence=px.colors.sequential.Viridis,
                title="Total do Portifólio por Categoria",
            )
            fig.update_layout(
                font=dict(family="Arial", size=15, color="White"),
                # paper_bgcolor="rgba(0,0,0,0)",
                # plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", tickvals=[], ticktext=[]),
                yaxis=dict(title=""),
                showlegend=False,
                uniformtext_minsize=8,
                uniformtext_mode="hide",
            )
            fig.update_traces(textposition='auto',insidetextanchor = "middle")
            fig.update_yaxes(showgrid=False)
            fig.update_xaxes(showgrid=False)
            fig.data[0].marker.color = "#9966ff"
            fig.data[0].textfont.color = "white"
            st.plotly_chart(fig,use_container_width=True)
        except:
            st.error("Você não possui um Portifólio nesta ferramenta")
    with chart1:
        if super_smart.empty:

            st.error("Você não possui um Portifólio nesta ferramenta")
        else:
        
            try:
                fig = px.bar(
                        super_smart[(super_smart["data"]>= inc) & (super_smart["data"]<= end)],
                        x="Mês",
                        y=subst,
                        color="label",
                        width=1000,
                        height=600,
                        text_auto='.2s',
                        title=f"Comissão Total Mensal",
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        labels = {"label":"Empresa",subst:subst+"(R$)"}
                    )
                fig.update_layout(
                    #showlegend=False,
                    legend_title= None,
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    # xanchor="right",
                    # x=0.2
                    )
                    )
                fig.update_traces(textfont_size=12,textposition='inside')
                temp=super_smart[(super_smart["data"]>= inc) & (super_smart["data"]<= end)]
                temp=temp[['Mês',subst]].groupby('Mês').sum().reset_index()
                fig.add_trace(go.Scatter(x=temp["Mês"], 
                    y=temp[subst],
                    text=round(temp[subst]).apply(lambda x: locale.currency(x, grouping=True,symbol=None)[:-3]),
                    mode='text',
                    textposition='top center',
                    textfont=dict(
                        size=12,
                    ),
                    showlegend=False,
                    hovertemplate='<extra></extra>'))
                
                fig.data[0].textfont.color = "white"
                fig.data[0].marker.color = "#9966ff"
                fig.data[1].marker.color = "#EBFF70"
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(title=None)
                #fig.update_traces(textposition="top center")
                st.plotly_chart(fig,use_container_width=True)
            except:
                fig = px.bar(
                        super_smart[(super_smart["data"]>= inc) & (super_smart["data"]<= end)],
                        x="Mês",
                        y=subst,
                        #color="label",
                        #width=1000,
                        height=600,
                        text_auto='.2s',
                        title=f"Comissão Total Mensal",
                        color_discrete_sequence=px.colors.sequential.Viridis,
                        labels = {"label":"Empresa",subst:subst+"(R$)"}
                    )
                fig.update_layout(
                    #showlegend=False,
                    legend_title= None,
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    showlegend=True,
                    legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    # xanchor="right",
                    # x=0.2,
                    )
                    )
                fig.update_traces(textfont_size=12,textposition='inside')
                temp=super_smart[(super_smart["data"]>= inc) & (super_smart["data"]<= end)]
                temp=temp[['Mês',subst]].groupby('Mês').sum().reset_index()
                fig.add_trace(go.Scatter(x=temp["Mês"], 
                    y=temp[subst],
                    text=round(temp[subst]).apply(lambda x: locale.currency(x, grouping=True,symbol=None)[:-3]),
                    mode='text',
                    textposition='top center',
                    textfont=dict(
                        size=12,
                    ),
                    showlegend=False,
                    hovertemplate='<extra></extra>'))
                
                fig.data[0].textfont.color = "white"
                fig.data[0].marker.color = "#EBFF70"
                fig.data[0]['showlegend']=True
                fig['data'][0]['name']=super_smart[(super_smart["data"]>= inc) & (super_smart["data"]<= end)]['label'].iloc[0]
                #fig.data[1].marker.color = "#EBFF70"
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(title=None)
                #fig.update_traces(textposition="top center")
                st.plotly_chart(fig,use_container_width=True)

if st.button('Logout',key='logout2'):
    st.session_state["logout"] =None
    if st.session_state["logout"]==None:
        nav_page('')
