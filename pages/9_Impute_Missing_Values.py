import streamlit as st
import pandas as pd

st.set_page_config(page_title="Impute Missing Values", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Impute Missing Values</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        columns_with_missing = data.columns[data.isnull().any()].tolist()
        
        if columns_with_missing:
            selected_column = st.selectbox("Select column to impute", options=columns_with_missing)
            dtype = data[selected_column].dtype
            
            if pd.api.types.is_numeric_dtype(dtype):
                imputation_method = st.radio("Select imputation method", options=["Mean", "Median", "Mode", "Constant"])
            else:
                imputation_method = st.radio("Select imputation method", options=["Mode", "Constant"])
            
            if imputation_method == "Constant":
                constant_value = st.text_input("Enter constant value", value="")
            
            if st.button("Impute"):
                if imputation_method == "Mean" and pd.api.types.is_numeric_dtype(dtype):
                    data[selected_column].fillna(data[selected_column].mean(), inplace=True)
                elif imputation_method == "Median" and pd.api.types.is_numeric_dtype(dtype):
                    data[selected_column].fillna(data[selected_column].median(), inplace=True)
                elif imputation_method == "Mode":
                    data[selected_column].fillna(data[selected_column].mode()[0], inplace=True)
                elif imputation_method == "Constant":
                    data[selected_column].fillna(constant_value, inplace=True)
                
                st.success(f"Missing values in column '{selected_column}' have been imputed using {imputation_method.lower()} method.")
                st.session_state['data'] = data
                
                st.write("Updated Data:")
                st.dataframe(data)
                
                csv = data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download updated data as CSV",
                    data=csv,
                    file_name='updated_data.csv',
                    mime='text/csv',
                )
        else:
            st.write("No columns with missing values available for imputation.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()