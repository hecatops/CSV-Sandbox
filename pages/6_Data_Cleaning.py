import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

st.set_page_config(page_title="Data Cleaning", page_icon="🧹", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
class DataQualityChecker:
    def __init__(self, data):
        self.data = data.copy()
        self.original_shape = data.shape
        
    def get_duplicate_info(self):
        """Get information about duplicate rows."""
        duplicates = self.data.duplicated(keep='first')
        duplicate_rows = self.data[duplicates]
        return {
            'total_duplicates': len(duplicate_rows),
            'duplicate_rows': duplicate_rows,
            'duplicate_indices': duplicates
        }
    
    def remove_duplicates(self, subset=None, keep='first'):
        """Remove duplicate rows."""
        self.data = self.data.drop_duplicates(subset=subset, keep=keep)
        return self.data
    
    def get_missing_info(self):
        """Get information about missing values."""
        missing_count = self.data.isnull().sum()
        missing_percent = (missing_count / len(self.data)) * 100
        missing_info = pd.DataFrame({
            'Missing Count': missing_count,
            'Missing Percentage': missing_percent
        })
        return missing_info[missing_info['Missing Count'] > 0]
    
    def handle_missing_values(self, strategy_dict):
        """Handle missing values according to specified strategies."""
        df = self.data.copy()
        
        for column, strategy in strategy_dict.items():
            if strategy == 'Drop rows':
                df = df.dropna(subset=[column])
            elif strategy == 'Mean':
                df[column] = df[column].fillna(df[column].mean())
            elif strategy == 'Median':
                df[column] = df[column].fillna(df[column].median())
            elif strategy == 'Mode':
                df[column] = df[column].fillna(df[column].mode()[0])
            elif strategy == 'Forward fill':
                df[column] = df[column].fillna(method='ffill')
            elif strategy == 'Backward fill':
                df[column] = df[column].fillna(method='bfill')
            elif strategy.startswith('Custom value:'):
                custom_value = strategy.split(':')[1].strip()
                df[column] = df[column].fillna(custom_value)
        
        self.data = df
        return df

def main():
    st.markdown("<h1 class='custom-sub'>Data Cleaning</h1>", unsafe_allow_html=True)
    
    if 'data' not in st.session_state:
        st.warning("Please upload your data first.")
        return
    
    checker = DataQualityChecker(st.session_state['data'])
    
    tab_duplicate, tab_missing = st.tabs(["Duplicate Detection", "Missing Value Analysis"])

    col1, col2 = st.columns([6, 1])
    with col2:
        csv = checker.data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned Data",
            data=csv,
            file_name='cleaned_data.csv',
            mime='text/csv'
        )
        
    with tab_duplicate:
        st.markdown("### Duplicate Row Detection")

        cols_for_duplicate = st.multiselect(
            "Select columns to consider for duplicates (empty for all columns)",
            options=checker.data.columns.tolist(),
            default=None
        )
        
        keep_option = st.radio(
            "Which duplicates to keep?",
            options=['first', 'last', 'none'],
            help="'first' keeps first occurrence, 'last' keeps last occurrence, 'none' removes all duplicates",
            horizontal=True
        )
        
        if st.button("Find Duplicates", type="primary"):
            duplicate_info = checker.get_duplicate_info()
            
            if duplicate_info['total_duplicates'] > 0:
                st.markdown(f"Found {duplicate_info['total_duplicates']} duplicate rows")
                st.dataframe(duplicate_info['duplicate_rows'], use_container_width=True)
                
                if st.button("Remove Duplicates", type="secondary"):
                    cleaned_data = checker.remove_duplicates(
                        subset=cols_for_duplicate if cols_for_duplicate else None,
                        keep=keep_option
                    )
                    st.session_state['data'] = cleaned_data
                    st.success(f"Removed {duplicate_info['total_duplicates']} duplicate rows")
                    st.dataframe(cleaned_data.head(), use_container_width=True)
            else:
                st.success("No duplicates found!")
    
    with tab_missing:
        st.markdown("### Missing Value Analysis")
        
        missing_info = checker.get_missing_info()
        if not missing_info.empty:
            st.markdown("#### Missing Value Statistics")
            st.dataframe(missing_info, use_container_width=True)
            
            st.markdown("#### Handle Missing Values")
            
            missing_strategies = {
                'numeric': ['Drop rows', 'Mean', 'Median', 'Forward fill', 'Backward fill', 'Custom value'],
                'categorical': ['Drop rows', 'Mode', 'Forward fill', 'Backward fill', 'Custom value']
            }
            
            strategy_dict = {}
            for column in missing_info.index:
                col1, col2 = st.columns([3, 1])
                col_type = 'numeric' if pd.api.types.is_numeric_dtype(checker.data[column]) else 'categorical'
                strategies = missing_strategies[col_type]
                
                with col1:
                    strategy = st.selectbox(
                        f"How to handle missing values in {column}?",
                        options=strategies,
                        key=f"strategy_{column}"
                    )
                
                with col2:
                    if strategy == 'Custom value':
                        custom_value = st.text_input(f"Enter custom value for {column}")
                        strategy = f"Custom value: {custom_value}"
                
                strategy_dict[column] = strategy
            
            if st.button("Apply Missing Value Handling", type="primary"):
                cleaned_data = checker.handle_missing_values(strategy_dict)
                st.session_state['data'] = cleaned_data
                st.success("Successfully handled missing values!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### Before Cleaning")
                    st.dataframe(missing_info, use_container_width=True)
                with col2:
                    st.markdown("#### After Cleaning")
                    new_missing_info = DataQualityChecker(cleaned_data).get_missing_info()
                    st.dataframe(new_missing_info if not new_missing_info.empty 
                               else pd.DataFrame({"Message": ["No missing values!"]}),
                               use_container_width=True)
        else:
            st.success("No missing values found in the dataset!")

if __name__ == "__main__":
    main()