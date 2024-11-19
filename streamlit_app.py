import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from local_components import card_container

st.set_page_config(page_title="Home", page_icon="✨", layout="wide")
# CSS styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

if 'data' not in st.session_state:
    st.session_state['data'] = None

@st.cache_data
def load_spotify_sample():
    try:
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                st.session_state['data'] = pd.read_csv('spotify_songs.csv', encoding=encoding)
                return pd.read_csv('spotify_songs.csv', encoding=encoding)
            except UnicodeDecodeError:
                continue
        st.error("Could not read file with any supported encoding")
        return None
    except Exception as e:
        st.error(f"Error loading sample dataset: {str(e)}")
        return None

if 'data' not in st.session_state:
    st.session_state['data'] = load_spotify_sample()
    
@st.cache_data
def read_csv(file, encoding='utf-8'):
    try:
        st.session_state['data'] = pd.read_csv(file, encoding=encoding)
        return pd.read_csv(file, encoding=encoding)
    except UnicodeDecodeError:
        encodings = ['latin1', 'iso-8859-1', 'cp1252']
        for enc in encodings:
            try:
                st.session_state['data'] = pd.read_csv(file, encoding=enc)
                return pd.read_csv(file, encoding=enc)
            except UnicodeDecodeError:
                continue
        st.error("Could not read file with any supported encoding")
        return None
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty.")
        return None
    except pd.errors.ParserError:
        st.error("Error parsing the CSV file. Please check if it's properly formatted.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while reading the file: {str(e)}")
        return None

st.markdown("<h1 class='custom-header'>What's in my CSV?</h1>", unsafe_allow_html=True)

# Sidebar for file upload and sample data
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    use_sample = st.button("Use Spotify Dataset")
    
    # Add encoding selector
    if uploaded_file is not None:
        encoding = st.selectbox(
            "Select file encoding",
            ['utf-8', 'latin1', 'iso-8859-1', 'cp1252'],
            index=0
        )

# Load data based on user choice
df = None or st.session_state['data']
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
    except Exception as e:
        st.error(f"Error with selected encoding. Trying alternative encodings...")
        df = read_csv(uploaded_file)
elif use_sample:
    df = load_spotify_sample()
    if df is not None:
        st.success("Loaded Spotify dataset!")

if df is not None and not df.empty:
    # Display basic metrics
    st.markdown("<h1 class='custom-sub'>Shape of Data</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    
    metrics = [
        ("Rows", df.shape[0]),
        ("Columns", df.shape[1]),
        ("Null Values", df.isnull().sum().sum())
    ]
    for col, (title, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""<div class="metric-card"><h2>{title}</h2><p>{value}</p></div>""",
                unsafe_allow_html=True
            )
    st.session_state['data'] = df
