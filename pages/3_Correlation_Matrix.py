import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import numpy as np

st.set_page_config(page_title="Correlation Matrix", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():    
    st.markdown("<h1 class='custom-sub'>Correlation Matrix</h1>", unsafe_allow_html=True)
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        numerical_data = data.select_dtypes(include=[np.number])
        
        if not numerical_data.empty:
            corr_matrix = numerical_data.corr()
            
            fig, ax = plt.subplots(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="twilight", center=0, ax=ax)
            ax.set_title("Correlation Matrix", color='white')
            fig.patch.set_facecolor('#0E1117')
            ax.set_facecolor('#0E1117')
            ax.set_yticklabels(ax.get_yticklabels(), rotation=0, color="white")
            ax.set_xticklabels(ax.get_xticklabels(), rotation=90, color="white")
            
            cbar = ax.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
            
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(
                label="Download plot as PNG",
                data=buf,
                file_name="correlation_matrix.png",
                mime="image/png",
            )
        else:
            st.write("No numerical columns available for correlation matrix.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()