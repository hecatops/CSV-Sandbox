import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures
import time

st.set_page_config(page_title="Custom Plots", page_icon="📈", layout="wide")

# Load CSS styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def plot_data(plot_type, data, x_axis, y_axis):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if plot_type == "Scatter Plot":
        sns.scatterplot(x=data[x_axis], y=data[y_axis], ax=ax)
    elif plot_type == "Line Plot":
        sns.lineplot(x=data[x_axis], y=data[y_axis], ax=ax)
    elif plot_type == "Bar Plot":
        sns.barplot(x=data[x_axis], y=data[y_axis], ax=ax)
    
    ax.set_title(f'{plot_type} of {x_axis} vs {y_axis}', color='white', fontsize=16)
    ax.set_xlabel(x_axis, color='white', fontsize=14)
    ax.set_ylabel(y_axis, color='white', fontsize=14)
    ax.set_facecolor('#0E1117')
    fig.patch.set_facecolor('#0E1117')
    ax.tick_params(axis='x', colors='white', labelsize=12, rotation=45)
    ax.tick_params(axis='y', colors='white', labelsize=12)
    
    plt.tight_layout()
    return fig

def main():
    st.markdown("<h1 class='custom-sub'>Custom Plots</h1>", unsafe_allow_html=True)
    
    # Access data from session state
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        # Select only numeric columns
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_columns:
            # Select columns for X and Y axes
            x_axis = st.selectbox("Select X axis", options=numeric_columns)
            y_axis = st.selectbox("Select Y axis", options=numeric_columns)
            
            # Select plot type
            plot_type = st.radio("Select plot type", options=["Scatter Plot", "Line Plot", "Bar Plot"])
            
            # Add Plot button
            if st.button("Plot"):
                with st.spinner('Generating plot...'):
                    try:
                        with concurrent.futures.ThreadPoolExecutor() as executor:
                            future = executor.submit(plot_data, plot_type, data, x_axis, y_axis)
                            fig = future.result(timeout=10)  # Set timeout in seconds
                            st.pyplot(fig)
                    except concurrent.futures.TimeoutError:
                        st.error("Plotting took too long. Please try with a smaller dataset or different parameters.")
        else:
            st.write("No numerical columns available for plotting.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()