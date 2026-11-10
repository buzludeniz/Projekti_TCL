import os

import streamlit as st
import pandas as pd
import oracledb
import matplotlib.pyplot as plt
import plotly.express as px

# --- KONFIGURIMI I LIDHJES ---
# Kredencialet lexohen nga variablat e mjedisit (ose nga skedari .env, nese
# python-dotenv eshte i instaluar). Mos i shkruani fjalekalimet ne kod.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def load_db_config():
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    if not user or not password:
        st.error(
            "Mungojne DB_USER dhe/ose DB_PASSWORD. Kopjoni .env.example ne .env "
            "dhe plotesoni vlerat (shih README.md)."
        )
        st.stop()
    config = {
        "user": user,
        "password": password,
        "dsn": os.environ.get("DB_DSN", "localhost:1521/XEPDB1"),
    }
    if os.environ.get("DB_SYSDBA", "false").strip().lower() in ("1", "true", "yes"):
        config["mode"] = oracledb.SYSDBA
    return config


DB_CONFIG = load_db_config()

# --- FUNKSIONE PER DATABASE ---
def get_data():
    try:
        conn = oracledb.connect(**DB_CONFIG)
        query = "SELECT ID_SHITJE, PRODUKTI, SHUMA, DATA_SH, PERDORUESI FROM Shitjet ORDER BY DATA_SH DESC"
        df = pd.read_sql(query, conn)
        df['DATA_SH'] = pd.to_datetime(df['DATA_SH'])
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def insert_sale(produkti, shuma, shitesi):
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Thirrja e procedures sipas skriptit SQL
        cursor.callproc("shto_transaksion_shitje", [produkti, shuma, shitesi])
        conn.close()
        return True
    except Exception as e:
        return False

def delete_sale(id_shitje, user):
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # KORRIGJIM: Emri i procedures duhet te jete i njejte me SQL Master Script
        cursor.callproc("fshi_transaksion_shitje", [id_shitje, user])
        conn.close()
        return True
    except Exception as e:
        st.error(f"Detajet e gabimit: {e}")
        return False

# --- CONFIG STREAMLIT ---
st.set_page_config(page_title="Dashboard TCL Pro", layout="wide")

# --- CUSTOM CSS PER UI MODERNE DHE KONTRAST TE LARTE ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] > div {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    div[data-testid="stMetricLabel"] > div {
        color: #64748b !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
        color: #475569 !important;
        border: 1px solid #e2e8f0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #007bff !important;
        color: #ffffff !important;
        border-color: #007bff !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #007bff;
        color: #ffffff !important;
        font-weight: bold;
        border: none;
    }
    label {
        color: #334155 !important;
        font-weight: 500 !important;
    }
    div[data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        color: #1e293b !important;
    }
    p {
        color: #334155 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("Sistemi i Menaxhimit te Shitjeve")
st.markdown("Monitorimi dhe kontrolli i transaksioneve ne kohe reale me arkitekture Oracle.")

df_main = get_data()

# --- METRICS SECTION ---
if not df_main.empty:
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Shitje", f"{df_main['SHUMA'].sum():,.2f} €")
    with m2:
        st.metric("Transaksione", len(df_main))
    with m3:
        try:
            top_prod = df_main.groupby('PRODUKTI')['SHUMA'].sum().idxmax()
        except:
            top_prod = "N/A"
        st.metric("Produkti Top", top_prod)
    with m4:
        st.metric("Mesatarja", f"{df_main['SHUMA'].mean():,.2f} €")

st.markdown("<br>", unsafe_allow_html=True)

tabs = st.tabs(["Menaxhimi i Te Dhenave", "Analiza dhe Grafikete", "Info & Dokumentacioni"])

# --- TABI MENAXHIMI ---
with tabs[0]:
    col_left, col_right = st.columns([1, 1.8], gap="large")

    with col_left:
        st.subheader("Veprime")
        
        with st.expander("Shto Regjistrim te Ri", expanded=True):
            prod = st.text_input("Emri i Produktit", placeholder="Shkruani emrin...")
            vlefta = st.number_input("Vlera (€)", min_value=0.0, step=1.0)
            user_list = ["Gridi_Admin", "Ergi_Dev", "Nataniel_Analyst"]
            shitesi = st.selectbox("Perdoruesi", user_list)
            
            if st.button("Ruaj Transaksionin"):
                if prod and vlefta > 0:
                    if insert_sale(prod, vlefta, shitesi):
                        st.success("Transaksioni u ruajt.")
                        st.rerun()
                    else:
                        st.error("Gabim gjate thirrjes se procedures.")
                else:
                    st.warning("Plotesoni te dhenat.")

        with st.expander("Fshirja e Regjistrimeve"):
            if not df_main.empty:
                sale_to_del = st.selectbox("Zgjidh ID per fshirje", df_main['ID_SHITJE'].unique())
                del_user = st.selectbox("Autorizuar nga", user_list, key="del_user")
                if st.button("Fshi Perfundimisht", type="secondary"):
                    if delete_sale(int(sale_to_del), del_user):
                        st.success("Regjistrimi u fshi me sukses.")
                        st.rerun()
                    else:
                        st.error("Procedura e fshirjes deshtoi. Kontrolloni nese ID ekziston.")
            else:
                st.info("Nuk ka regjistrime per te fshire.")

    with col_right:
        st.subheader("Pasqyra e Fundit")
        if not df_main.empty:
            st.dataframe(
                df_main.style.format({"SHUMA": "{:.2f} €"}),
                use_container_width=True,
                height=500
            )
        else:
            st.info("Nuk ka te dhena ne sistem.")

# --- TABI ANALITIKA ---
with tabs[1]:
    if not df_main.empty:
        st.subheader("Vizualizimi i Performancave")
        c1, c2 = st.columns(2)
        
        with c1:
            df_bar = df_main.groupby('PRODUKTI')['SHUMA'].sum().reset_index()
            fig_bar = px.bar(df_bar, x='PRODUKTI', y='SHUMA', 
                             title="Shitjet sipas Produktit",
                             color='SHUMA', color_continuous_scale='Blues',
                             template='plotly_white')
            st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            df_pie = df_main.groupby('PERDORUESI')['SHUMA'].sum().reset_index()
            fig_pie = px.pie(df_pie, values='SHUMA', names='PERDORUESI', 
                             title="Shperndarja sipas Stafit",
                             hole=0.4,
                             template='plotly_white')
            st.plotly_chart(fig_pie, use_container_width=True)
            
        # FIX per Pylance reportAttributeAccessIssue:
        # Perdorim konvertim eksplicit ne datetime dhe floor('D') per nxjerrjen e dates
        df_temp = df_main.copy()
        df_temp['DATA_KONTROLLI'] = pd.to_datetime(df_temp['DATA_SH']).dt.normalize()
        df_time = df_temp.groupby('DATA_KONTROLLI')['SHUMA'].sum().reset_index()
        df_time = df_time.sort_values('DATA_KONTROLLI')
        
        fig_line = px.line(df_time, x='DATA_KONTROLLI', y='SHUMA', 
                           title="Trendi i Shitjeve ne Kohe (Sipas Dates)", 
                           markers=True,
                           template='plotly_white',
                           labels={'DATA_KONTROLLI': 'Data', 'SHUMA': 'Vlera Totale (€)'})
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Nuk ka te dhena per te gjeneruar analitike.")

# --- TABI DOKUMENTACIONI ---
with tabs[2]:
    c_inf1, c_inf2 = st.columns(2)
    with c_inf1:
        st.markdown("""
        ### Arkitektura e Sistemit
        Ky dashboard sherben si nje nderfaqe vizuale per nje baze te dhenash Oracle. 
        Sistemi eshte i ndertuar per te suportuar transaksione te sigurta (TCL).
        
        - **Baza e te dhenave:** Oracle XE (Localhost)
        - **Procedura e Fshirjes:** `fshi_transaksion_shitje`
        - **UI:** Streamlit Framework
        """)
    
    with c_inf2:
        st.markdown("""
        ### Logjika e Biznesit
        - **Commit/Rollback:** Implementuar ne nivel procedure SQL.
        - **Auditimi:** Cdo veprim regjistrohet ne tabelen `Audit_Log`.
        - **Validimi:** Kontrolli i vlerave pozitive kryhet ne Database.
        """)

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Dashboard TCL Professional | 2024")