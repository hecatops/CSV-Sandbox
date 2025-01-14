import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Outlier Detection", page_icon="🔮", layout="wide")

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

def detect_outliers_mad(data, column, threshold=3.5):
    median = np.median(data[column])
    mad = np.median(np.abs(data[column] - median))
    modified_zscore = 0.6745 * (data[column] - median) / mad
    return data[np.abs(modified_zscore) > threshold]

def remove_outliers(data, column, method, threshold=3.5):
    if method == "Z-score":
        mean = np.mean(data[column])
        std = np.std(data[column])
        z_scores = (data[column] - mean) / std
        return data[np.abs(z_scores) <= threshold]
    elif method == "IQR":
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    else:
        median = np.median(data[column])
        mad = np.median(np.abs(data[column] - median))
        modified_zscore = 0.6745 * (data[column] - median) / mad
        return data[np.abs(modified_zscore) <= threshold]

def main():
    st.markdown("<h1 class='custom-sub'>Outlier Detection</h1>", unsafe_allow_html=True)

    if 'data' in st.session_state:
        data = st.session_state['data']
        numeric_columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_columns:
            selected_column = st.selectbox("Select column for outlier detection", options=numeric_columns)
            
            method = st.radio("Select outlier detection method", options=["Z-score", "IQR", "MAD"])
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Detect Outliers"):
                    if method == "Z-score":
                        outliers = detect_outliers_zscore(data, selected_column)
                    elif method == "IQR":
                        outliers = detect_outliers_iqr(data, selected_column)
                    else:  # MAD
                        outliers = detect_outliers_mad(data, selected_column)
                    
                    st.markdown("### Outliers")
                    st.dataframe(outliers)
                    
                    csv = outliers.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download outliers data as CSV",
                        data=csv,
                        file_name='outliers_data.csv',
                        mime='text/csv',
                    )
            
            with col2:
                if st.button("Remove Outliers"):
                    cleaned_data = remove_outliers(data, selected_column, method)
                    st.session_state['data'] = cleaned_data
                    
                    st.markdown("### Cleaned Data")
                    st.dataframe(cleaned_data)
                    
                    csv = cleaned_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download cleaned data as CSV",
                        data=csv,
                        file_name='cleaned_data.csv',
                        mime='text/csv',
                    )
        else:
            st.write("No numerical columns available for outlier detection.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()