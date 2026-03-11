import pandas as pd 
import streamlit as st

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame()

st.set_page_config(
    page_title="pH-Rechner App",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

pg_home = st.Page("views/home.py", title="Home", icon=":material/home:", default=True)
pg_rechner = st.Page("views/pH-Rechner_views.py", title="pH-Rechner", icon=":material/science:")

pg = st.navigation([pg_home, pg_rechner])
pg.run()
