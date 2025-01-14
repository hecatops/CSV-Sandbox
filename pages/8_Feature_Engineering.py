import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Feature Selection", page_icon="⛏️", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_lasso_feature_importance(X, y, alpha=1.0):
    """Calculate feature importance using Lasso regularization."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = Lasso(alpha=alpha)
    model.fit(X_scaled, y)
    
    importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': np.abs(model.coef_)
    })
    return importance.sort_values('Importance', ascending=False)

def get_tree_feature_importance(X, y):
    """Calculate feature importance using Random Forest."""
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    })
    return importance.sort_values('Importance', ascending=False)

def get_correlation_importance(X, y, threshold=0.0):
    """Calculate feature importance using absolute correlation with target."""
    # Add target to dataframe for correlation calculation
    df = X.copy()
    df['target'] = y
    
    # Calculate correlations with target
    correlations = df.corr()['target'].drop('target')
    
    importance = pd.DataFrame({
        'Feature': correlations.index,
        'Importance': np.abs(correlations.values)
    })
    return importance.sort_values('Importance', ascending=False)

def plot_feature_importance(importance_df, title):
    """Plot feature importance."""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=importance_df, x='Importance', y='Feature')
    plt.title(title)
    plt.tight_layout()
    return plt

def main():
    st.markdown("<h1 class='custom-sub'>Feature Engineering</h1>", unsafe_allow_html=True)
    
    if 'data' not in st.session_state:
        st.warning("Please upload your data first.")
        return
    
    data = st.session_state['data']
    
    # Get numeric columns
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Not enough numeric columns for feature selection.")
        return
    
    target_variable = st.selectbox(
        "Select target variable",
        options=numeric_cols,
        key="target_var"
    )
    
    feature_cols = [col for col in numeric_cols if col != target_variable]
    
    method = st.radio(
        "Select feature selection method",
        ["Lasso", "Tree-based", "Correlation"]
    )
    
    if method == "Lasso":
        alpha = st.slider("Select Lasso alpha", 0.01, 10.0, 1.0)
    elif method == "Correlation":
        correlation_threshold = st.slider("Select correlation threshold", 0.0, 1.0, 0.0)
    
    max_features = len(feature_cols)
    n_features = st.slider("Number of features to select", 1, max_features, max_features)
    
    if st.button("Run Feature Selection"):
        X = data[feature_cols]
        y = data[target_variable]
        
        if method == "Lasso":
            importance_df = get_lasso_feature_importance(X, y, alpha)
        elif method == "Tree-based":
            importance_df = get_tree_feature_importance(X, y)
        else: 
            importance_df = get_correlation_importance(X, y, correlation_threshold)

        selected_features = importance_df.head(n_features)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.pyplot(plot_feature_importance(importance_df, f"Feature Importance using {method}"))
        
        with col2:
            st.markdown("### Selected Features")
            st.dataframe(selected_features)
        
        final_features = selected_features['Feature'].tolist() + [target_variable]
        selected_data = data[final_features]
        
        st.session_state['selected_features'] = final_features
        
        csv = selected_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download dataset with selected features",
            data=csv,
            file_name='selected_features_dataset.csv',
            mime='text/csv'
        )

        st.markdown("### Correlation Heatmap of Selected Features")
        plt.figure(figsize=(10, 8))
        sns.heatmap(selected_data.corr(), annot=True, cmap='coolwarm', center=0)
        plt.tight_layout()
        st.pyplot(plt)

if __name__ == "__main__":
    main()