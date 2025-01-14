import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import base64
from io import BytesIO

st.set_page_config(page_title="Train Test Split", page_icon="➗", layout="wide")


with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
def get_csv_download_link(df, filename):
    """Generate a download link for a DataFrame"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename}</a>'
    return href

def main():
    st.markdown("<h1 class='custom-sub'>Train Test Split</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        st.markdown("### Split Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            test_size = st.slider(
                "Test Set Size",
                min_value=0.1,
                max_value=0.4,
                value=0.2,
                step=0.05,
                help="Proportion of the dataset to include in the test split"
            )
            
            random_state = st.slider(
                "Random Seed",
                min_value=0,
                max_value=100,
                value=42,
                help="Seed for reproducibility"
            )
        
        with col2:
            include_validation = st.checkbox(
                "Include Validation Set",
                value=False,
                help="Split data into train, validation, and test sets"
            )
            
            if include_validation:
                validation_size = st.slider(
                    "Validation Set Size",
                    min_value=0.1,
                    max_value=0.3,
                    value=0.15,
                    step=0.05,
                    help="Proportion of the dataset to include in the validation split"
                )
 
        if st.button("Generate Split", type="primary"):
            if include_validation:
                train_val, test = train_test_split(
                    data,
                    test_size=test_size,
                    random_state=random_state
                )
            
                val_size_adjusted = validation_size / (1 - test_size)
                train, val = train_test_split(
                    train_val,
                    test_size=val_size_adjusted,
                    random_state=random_state
                )
 
                st.markdown("### Split Results")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Training Set Size", f"{len(train)} samples", 
                             f"{len(train)/len(data):.1%} of data")
                with col2:
                    st.metric("Validation Set Size", f"{len(val)} samples",
                             f"{len(val)/len(data):.1%} of data")
                with col3:
                    st.metric("Test Set Size", f"{len(test)} samples",
                             f"{len(test)/len(data):.1%} of data")
                
                st.markdown("### Download Split Datasets")
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                with dl_col1:
                    st.markdown(get_csv_download_link(train, "train_set"), unsafe_allow_html=True)
                with dl_col2:
                    st.markdown(get_csv_download_link(val, "validation_set"), unsafe_allow_html=True)
                with dl_col3:
                    st.markdown(get_csv_download_link(test, "test_set"), unsafe_allow_html=True)
                
            else:
                train, test = train_test_split(
                    data,
                    test_size=test_size,
                    random_state=random_state
                )
                
                st.markdown("### Split Results")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Training Set Size", f"{len(train)} samples",
                             f"{len(train)/len(data):.1%} of data")
                with col2:
                    st.metric("Test Set Size", f"{len(test)} samples",
                             f"{len(test)/len(data):.1%} of data")
                
                st.markdown("### Download Split Datasets")
                dl_col1, dl_col2 = st.columns(2)
                with dl_col1:
                    st.markdown(get_csv_download_link(train, "train_set"), unsafe_allow_html=True)
                with dl_col2:
                    st.markdown(get_csv_download_link(test, "test_set"), unsafe_allow_html=True)
    
    else:
        st.write("No data available. Please upload a dataset first.")

if __name__ == "__main__":
    main()