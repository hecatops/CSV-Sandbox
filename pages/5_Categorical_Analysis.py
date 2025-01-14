import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Categorical Analysis", page_icon="🐈‍⬛", layout="wide")

# Load custom styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Categorical Analysis</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        # Identify truly categorical columns
        def is_categorical(column):
            num_unique = data[column].nunique()
            total_rows = len(data)
            dtype = data[column].dtype
            return num_unique <= 0.1 * total_rows and dtype == "object"
        
        categorical_columns = [col for col in data.columns if is_categorical(col)]
        
        if categorical_columns:
            # Select a categorical column
            selected_column = st.selectbox("Select column for categorical analysis", options=categorical_columns)
            
            # Generate summary statistics
            summary_stats = data[selected_column].describe()
            
            # Create frequency table with repeat count
            counts = data[selected_column].value_counts()
            proportions = counts / len(data)
            repeat_count = counts.apply(lambda x: f"{x} occurrences") 
            frequency_table = pd.DataFrame({
                "Category": counts.index,
                "Count": counts.values,
                "Proportion": proportions.values,
                "Repeat Count": repeat_count.values  
            })
            st.write(frequency_table)

        else:
            st.write("No columns satisfy the categorical criteria for analysis.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()