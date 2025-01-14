import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Head", page_icon="🎩", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>Data Head</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        st.write("Click on any column header to sort by that value.")
        st.dataframe(data.head(20))
    else:
        st.write("No data available.")


if __name__ == "__main__":
    main()