import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="PCA Analysis", page_icon="✨", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    st.markdown("<h1 class='custom-sub'>PCA Analysis</h1>", unsafe_allow_html=True)
    
    if 'data' in st.session_state:
        data = st.session_state['data']
        
        numeric_data = data.select_dtypes(include=[np.number])
        
        if not numeric_data.empty:
            standardized_data = (numeric_data - numeric_data.mean()) / numeric_data.std()
            
            if standardized_data.shape[1] < 2:
                st.write("Not enough numerical columns available for PCA.")
            else:
                n_components = st.slider("Select number of PCA components", min_value=1, max_value=min(10, standardized_data.shape[1]), value=2)
                
                if st.button("Start PCA"):
                    try:
                        pca = PCA(n_components=n_components)
                        principal_components = pca.fit_transform(standardized_data)
                        explained_variance = pca.explained_variance_ratio_
                        
                        pca_df = pd.DataFrame(data=principal_components, columns=[f'PC{i+1}' for i in range(n_components)])
                        
                        st.markdown("### Explained Variance Ratio")
                        st.write(explained_variance)
                        
                        if n_components == 2:
                            fig, ax = plt.subplots(figsize=(10, 6))
                            sns.scatterplot(x=pca_df['PC1'], y=pca_df['PC2'], ax=ax)
                            ax.set_title('PCA: PC1 vs PC2', color='white')
                            ax.set_xlabel('PC1', color='white')
                            ax.set_ylabel('PC2', color='white')
                            ax.set_facecolor('#0E1117')
                            fig.patch.set_facecolor('#0E1117')
                            ax.tick_params(axis='x', colors='white')
                            ax.tick_params(axis='y', colors='white')
                            st.pyplot(fig)
                        elif n_components == 3:
                            fig = plt.figure(figsize=(10, 6))
                            ax = fig.add_subplot(111, projection='3d')
                            ax.scatter(pca_df['PC1'], pca_df['PC2'], pca_df['PC3'])
                            ax.set_title('PCA: PC1 vs PC2 vs PC3', color='white')
                            ax.set_xlabel('PC1', color='white')
                            ax.set_ylabel('PC2', color='white')
                            ax.set_zlabel('PC3', color='white')
                            ax.set_facecolor('#0E1117')
                            fig.patch.set_facecolor('#0E1117')
                            ax.tick_params(axis='x', colors='white')
                            ax.tick_params(axis='y', colors='white')
                            ax.tick_params(axis='z', colors='white')
                            st.pyplot(fig)
                        else:
                            st.write("PCA plot is only available for 2 or 3 components.")
                        
                        st.markdown("### Principal Components")
                        st.dataframe(pca_df)
                        
                        csv = pca_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download PCA data as CSV",
                            data=csv,
                            file_name='pca_data.csv',
                            mime='text/csv',
                        )
                    except Exception as e:
                        st.error("PCA cannot be performed with the given parameters. Please try cleaning your data or trying manually.")
        else:
            st.write("No numerical columns available for PCA.")
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()