import pandas as pd 
import streamlit as st

# --- NEW CODE: import and initialize data manager and login manager ---
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

data_manager = DataManager(       # initialize data manager
    fs_protocol='webdav',         # protocol for the filesystem, use webdav for switch drive
    fs_root_folder="BMLD_App_DB"  # folder on switch drive where the data is stored
    ) 
login_manager = LoginManager(data_manager) # handles user login and registration
login_manager.login_register()             # stops if not logged in

if 'data_df' not in st.session_state:
    st.session_state['data_df'] = data_manager.load_user_data(
        'data.csv',                     # The file on switch drive where the data is stored
        initial_value=pd.DataFrame(),   # Initial value if the file does not exist
        parse_dates=['timestamp']       # Parse timestamp as datetime
    )
# --- END OF CODE UPDATE ---

#ALTER CODE:
#if 'data_df' not in st.session_state:
#    st.session_state['data_df'] = pd.DataFrame()

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
