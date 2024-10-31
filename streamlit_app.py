import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from local_components import card_container

st.set_page_config(layout="wide")

# CSS styles
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
        font-size: 9rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    .custom-sub {
        background: linear-gradient(to right, #00bbf9, #caf0f8);
        -webkit-text-fill-color: transparent;
        -webkit-background-clip: text;
        font-size: 3rem;
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
        font-size: 2rem;
    }
    .metric-card p {
        font-size: 5rem;
        color: #caf0f8;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_spotify_sample():
    try:
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                return pd.read_csv('spotify_songs.csv', encoding=encoding)
            except UnicodeDecodeError:
                continue
        st.error("Could not read file with any supported encoding")
        return None
    except Exception as e:
        st.error(f"Error loading sample dataset: {str(e)}")
        return None

@st.cache_data
def read_csv(file, encoding='utf-8'):
    try:
        return pd.read_csv(file, encoding=encoding)
    except UnicodeDecodeError:
        encodings = ['latin1', 'iso-8859-1', 'cp1252']
        for enc in encodings:
            try:
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

def parse_df_info(df):
    try:
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
                
                min_val, max_val = get_column_bounds(df, col_name)
                parsed_data.append([str(col_number), col_name, non_null, dtype, str(min_val), str(max_val)])
                col_number += 1

        return pd.DataFrame(parsed_data, columns=['#', 'Column', 'Non-Null Count', 'Dtype', 'Min', 'Max'])
    except Exception as e:
        st.error(f"Error parsing DataFrame info: {str(e)}")
        return pd.DataFrame()

def get_column_bounds(df, col_name):
    try:
        series = df[col_name]
        if series.empty:
            return 'N/A', 'N/A'
            
        if pd.api.types.is_numeric_dtype(series):
            return series.min(), series.max()
        elif pd.api.types.is_datetime64_any_dtype(series):
            return series.min(), series.max()
        elif pd.api.types.is_string_dtype(series):
            non_null = series.dropna()
            if non_null.empty:
                return 'N/A', 'N/A'
            return non_null.min(), non_null.max()
        else:
            return 'N/A', 'N/A'
    except Exception as e:
        return f'Error: {str(e)}', f'Error: {str(e)}'

def generate_correlation_plot(df):
    """Generate correlation heatmap using app's color scheme"""
    try:
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return None
        
        corr = numeric_df.corr()
        
        # Create custom color palette using app's colors
        colors = ['#1e1e1e', '#00bbf9', '#caf0f8']  # Dark to light blue
        custom_cmap = sns.color_palette(colors, as_cmap=True)
        
        plt.figure(figsize=(12, 8))
        
        # Customize the heatmap
        sns.heatmap(
            corr,
            annot=True,
            cmap=custom_cmap,
            center=0,
            vmin=-1,
            vmax=1,
            square=True,
            fmt='.2f',
            annot_kws={'size': 8},
            linewidths=0.5,
            cbar_kws={"shrink": .8}
        )
        
        plt.title('Correlation Matrix', pad=20, color='black')
        
        # Style the plot
        plt.xticks(rotation=45, ha='right', color='black')
        plt.yticks(rotation=0, color='black')
        
        # Set plot background to match app theme
        plt.gca().set_facecolor('#f0f0f0')
        plt.gcf().set_facecolor('#f0f0f0')
        
        plt.tight_layout()
        
        return plt.gcf()
    except Exception as e:
        st.error(f"Error generating correlation plot: {str(e)}")
        return None

def plot_date_column(df, col):
    """Plot time series data with error handling"""
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        df[col].value_counts().sort_index().plot(ax=ax)
        
        # Style the plot
        ax.set_facecolor('#1e1e1e')
        fig.set_facecolor('#1e1e1e')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        
        plt.tight_layout()
        return fig
    except Exception as e:
        st.error(f"Error plotting {col}: {str(e)}")
        return None

# Main app
st.markdown("<h1 class='custom-header'>What's in my CSV?</h1>", unsafe_allow_html=True)

# Sidebar for file upload and sample data
with st.sidebar:
    st.header("Upload or Use Sample Data")
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
df = None
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
        ("Number of Rows", df.shape[0]),
        ("Number of Columns", df.shape[1]),
        ("Number of Null Values", df.isnull().sum().sum())
    ]
    
    for col, (title, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""<div class="metric-card"><h2>{title}</h2><p>{value}</p></div>""",
                unsafe_allow_html=True
            )

    # Display data description
    st.markdown("<h1 class='custom-sub'>Description of Data</h1>", unsafe_allow_html=True)
    with card_container(key="table1"):
        info_df = parse_df_info(df)
        if not info_df.empty:
            ui.table(data=info_df, maxHeight=300)

    # Display data head
    st.markdown("<h1 class='custom-sub'>Head of Data</h1>", unsafe_allow_html=True)
    with card_container(key="table2"):
        try:
            ui.table(data=df.head(10), maxHeight=300)
        except Exception as e:
            st.error(f"Error displaying data head: {str(e)}")

    # Correlation Analysis
    st.markdown("<h1 class='custom-sub'>Correlation Analysis</h1>", unsafe_allow_html=True)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        fig = generate_correlation_plot(df)
        if fig:
            st.pyplot(fig)
    else:
        st.info("No numeric columns available for correlation analysis.")

    # Date Column Analysis
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if not date_cols.empty:
        st.markdown("<h1 class='custom-sub'>Time Series Analysis</h1>", unsafe_allow_html=True)
        for col in date_cols:
            st.subheader(f"Distribution of {col}")
            fig = plot_date_column(df, col)
            if fig:
                st.pyplot(fig)

else:
    st.info("Upload a CSV file or use the sample dataset to begin analysis.")
