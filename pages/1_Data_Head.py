import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Head", page_icon="✨", layout="wide")

# Load CSS styles
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Data Head</h1>", unsafe_allow_html=True)
    
    # Access data from session state
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        # Display the head of the data
        st.write("First 10 Rows of the Data:")
        st.dataframe(data.head(10))
    else:
        st.write("No data available.")


if __name__ == "__main__":
    main()