import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import matplotlib.pyplot as plt
import io
from local_components import card_container

st.set_page_config(layout="wide")
st.markdown("""
    <style>
    body, input, button, select, textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        font-size: 1.6rem;
    }
    .custom-header {
        background: linear-gradient(to right, #00bbf9, #caf0f8);
        -webkit-text-fill-color: transparent;
        -webkit-background-clip: text;
        font-size: 5rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .custom-sub {
        background: linear-gradient(to right, #00bbf9, #caf0f8);
        -webkit-text-fill-color: transparent;
        -webkit-background-clip: text;
        font-size: 2rem;

    }
    .metric-card {
        border-radius: 10px;
        box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.3);
        padding: 1rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        height: 100%;
    }
    .metric-card h2 {
        font-size: 1rem;
    }
    .metric-card p {
        font-size: 4rem;
        color: #caf0f8;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

def parse_df_maxx(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()
    
    lines = info_string.split('\n')
    parsed_data = []
    col_number = 1 
    
    for line in lines:
        parts = line.split()
        if len(parts) >= 4 and parts[0].isdigit(): 
            col_name = parts[1]
            non_null = f"{parts[2]} non-null"
            dtype = ' '.join(parts[3:])
            
            if df[col_name].dtype in ['int64', 'float64']:
                min_val = df[col_name].min()
                max_val = df[col_name].max()
            elif df[col_name].dtype == 'object':
                try:
                    min_val = df[col_name].min()
                    max_val = df[col_name].max()
                except TypeError:
                    min_val = 'N/A'
                    max_val = 'N/A'
            elif pd.api.types.is_datetime64_any_dtype(df[col_name]):
                min_val = df[col_name].min()
                max_val = df[col_name].max()
            else:
                min_val = 'N/A'
                max_val = 'N/A'
            
            parsed_data.append([str(col_number), col_name, non_null, dtype, str(min_val), str(max_val)])
            col_number += 1

    info_df = pd.DataFrame(parsed_data, columns=['#', 'Column', 'Non-Null Count', 'Dtype', 'Min', 'Max'])
    return info_df

uploaded_file = st.file_uploader("", type="csv", label_visibility="hidden")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            st.error("The uploaded CSV file is empty. Please upload a valid dataset.")
        else:    
            df_filled = df.fillna("N/A")
            
            df.columns = [f"Unnamed_Column_{i}" if "Unnamed" in col else col for i, col in enumerate(df.columns)]
        
            st.markdown("<h1 class='custom-sub'>Shape of Data</h1>", unsafe_allow_html=True)
            cols = st.columns(3)
            with cols[0]:
                with st.container():
                    st.markdown("""<div class="metric-card"><h2>Number of Rows</h2><p>{}</p></div>""".format(df.shape[0]), unsafe_allow_html=True)
            with cols[1]:    
                with st.container():
                    st.markdown("""<div class="metric-card"><h2>Number of Columns</h2><p>{}</p></div>""".format(df.shape[1]), unsafe_allow_html=True)
            with cols[2]:    
                with st.container():
                    st.markdown("""<div class="metric-card"><h2>Number of Null Values</h2><p>{}</p></div>""".format(df.isnull().sum().sum()), unsafe_allow_html=True)
        
            st.markdown("<h1 class='custom-sub'>Description of Data</h1>", unsafe_allow_html=True)
        
            with card_container(key="table1"):
                info_df = parse_df_maxx(df)
                ui.table(data=info_df, maxHeight=300)    
        
            st.markdown("<h1 class='custom-sub'>Head of Data</h1>", unsafe_allow_html=True)
            with card_container(key="table2"):
                ui.table(data=df_filled.head(10), maxHeight=300)
        
            date_cols = df.select_dtypes(include=['datetime64']).columns
            for col in date_cols:
                st.subheader(f"Line Chart for {col}")
                st.line_chart(df[col])
    except pd.errors.ParserError:
        st.error("There was an error parsing the CSV file. Please check the file format and try again.")
    
    except KeyError as e:
        st.error(f"Column {e} is missing from the dataset. Please check the dataset and try again.")
    
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}. Please try again with a different dataset.")
