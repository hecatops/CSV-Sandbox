import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Categorical Analysis", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Categorical Analysis</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        categorical_columns = data.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if categorical_columns:
            selected_column = st.selectbox("Select column for categorical analysis", options=categorical_columns)
            
            st.write(data[selected_column].describe())
            
        else:
            st.write("No categorical columns available for analysis.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()