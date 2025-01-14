import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

st.set_page_config(page_title="Distribution Analysis", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_color_gradient(color1, color2, n):
    cmap = LinearSegmentedColormap.from_list("gradient", [color1, color2], N=n)
    return [cmap(i) for i in range(n)]

def main():
    st.markdown("<h1 class='custom-sub'>Distribution Analysis</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
      
        numerical_columns = [
            col for col in data.select_dtypes(include=[np.number]).columns
            if 2 < data[col].nunique() < len(data) and (data[col].value_counts(normalize=True).max() < 0.9)
        ]
        
        if numerical_columns:
            selected_column = st.selectbox("Select column to view distribution", options=numerical_columns)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            n, bins, patches = ax.hist(data[selected_column].dropna(), bins=30, edgecolor='black')

            color1 = "#ffba49"
            color2 = "#20a39e"
            colors = get_color_gradient(color1, color2, len(patches))
            for patch, color in zip(patches, colors):
                patch.set_facecolor(color)
            
            ax.set_title(f'Distribution of {selected_column}', fontsize=14, color='white')
            ax.set_xlabel(selected_column, fontsize=14, color='white')
            ax.set_ylabel('Frequency', fontsize=14, color='white')
            ax.set_facecolor('#0E1117')
            fig.patch.set_facecolor('#0E1117')
            
            ax.grid(False)
            
            ax.tick_params(axis='x', colors='white', size=10, width=2)
            ax.tick_params(axis='y', colors='white', size=10, width=2)
            
            st.pyplot(fig)
        else:
            st.write("No numerical columns with a meaningful spread of values available.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()