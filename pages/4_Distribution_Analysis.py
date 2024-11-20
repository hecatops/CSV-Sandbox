import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Distribution Analysis", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Distribution Analysis</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
      
        numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numerical_columns:
            selected_column = st.selectbox("Select column to view distribution", options=numerical_columns)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(data[selected_column].dropna(), bins=30, color='skyblue', edgecolor='black')
            ax.set_title(f'Distribution of {selected_column}', color='white')
            ax.set_xlabel(selected_column, color='white')
            ax.set_ylabel('Frequency', color='white')
            ax.set_facecolor('#0E1117')
            fig.patch.set_facecolor('#0E1117')
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            
            st.pyplot(fig)
        else:
            st.write("No numerical columns available for distribution analysis.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()