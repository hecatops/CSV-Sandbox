import streamlit as st
import pandas as pd

st.set_page_config(page_title="Impute Missing Values", page_icon="🛠️", layout="wide")

# Load CSS styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Impute Missing Values</h1>", unsafe_allow_html=True)
    
    # Access data from session state
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        # Select columns with missing values
        columns_with_missing = data.columns[data.isnull().any()].tolist()
        
        if columns_with_missing:
            # Column selection
            selected_column = st.selectbox("Select column to impute", options=columns_with_missing)
            
            # Determine the data type of the selected column
            dtype = data[selected_column].dtype
            
            # Select imputation method based on data type
            if pd.api.types.is_numeric_dtype(dtype):
                imputation_method = st.radio("Select imputation method", options=["Mean", "Median", "Mode", "Constant"])
            else:
                imputation_method = st.radio("Select imputation method", options=["Mode", "Constant"])
            
            if imputation_method == "Constant":
                constant_value = st.text_input("Enter constant value", value="")
            
            # Add Impute button
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
                st.session_state['data'] = data  # Update session state with imputed data
                
                # Display the updated data
                st.write("Updated Data:")
                st.dataframe(data)
                
                # Provide download link for the updated data
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