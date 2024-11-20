import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Outlier Detection", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def detect_outliers_zscore(data, column, threshold=3):
    mean = np.mean(data[column])
    std = np.std(data[column])
    z_scores = (data[column] - mean) / std
    return data[np.abs(z_scores) > threshold]

def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data[column] < lower_bound) | (data[column] > upper_bound)]

def main():
    st.markdown("<h1 class='custom-sub'>Outlier Detection</h1>", unsafe_allow_html=True)

    if 'data' in st.session_state:
        data = st.session_state['data']
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_columns:
            selected_column = st.selectbox("Select column for outlier detection", options=numeric_columns)
            
            method = st.radio("Select outlier detection method", options=["Z-score", "IQR"])
            
            if st.button("Detect Outliers"):
                if method == "Z-score":
                    outliers = detect_outliers_zscore(data, selected_column)
                elif method == "IQR":
                    outliers = detect_outliers_iqr(data, selected_column)
                
                st.markdown("### Outliers")
                st.dataframe(outliers)
                
                csv = outliers.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download outliers data as CSV",
                    data=csv,
                    file_name='outliers_data.csv',
                    mime='text/csv',
                )
        else:
            st.write("No numerical columns available for outlier detection.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()