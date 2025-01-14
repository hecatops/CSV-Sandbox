import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

def get_color_gradient(color1, color2, n_colors):
    """Generate a gradient between two colors."""
    color1 = np.array(tuple(int(color1.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))) / 255.0
    color2 = np.array(tuple(int(color2.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))) / 255.0
    return [tuple(c) for c in np.linspace(color1, color2, n_colors)]

def plot_feature_importance(importance_df, title):
    """Plot feature importance with custom colors."""
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.set_facecolor('#0E1117')
    plt.gcf().set_facecolor('#0E1117')
    
    # Create bar plot
    bars = plt.barh(importance_df['Feature'], importance_df['Importance'])
    
    # Apply color gradient
    color1 = "#ffba49"
    color2 = "#20a39e"
    colors = get_color_gradient(color1, color2, len(bars))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.title(title, color='white')
    ax.tick_params(axis='both', colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    
    plt.tight_layout()
    return plt

def plot_correlation_heatmap(data):
    """Plot correlation heatmap with custom colors."""
    plt.figure(figsize=(10, 8))
    ax = plt.gca()
    ax.set_facecolor('#0E1117')
    plt.gcf().set_facecolor('#0E1117')
    
    # Custom colormap
    hex_colors = ["#ffba49", "#fff", "#20a39e", "#fff", "#ffba49"]
    custom_cmap = sns.color_palette(hex_colors, as_cmap=True)
    
    # Plot heatmap
    sns.heatmap(
        data.corr(),
        annot=True,
        cmap=custom_cmap,
        center=0,
        fmt='.2f',
        annot_kws={'color': 'black'},
        cbar_kws={'label': 'Correlation'}
    )
    
    # Style adjustments
    ax.tick_params(axis='both', colors='white')
    plt.title("Correlation Heatmap", color='white', pad=20)
    
    plt.tight_layout()
    return plt

# Update the main() function to use these new plotting functions
def main():
    # [Previous code remains the same until plotting section]
    
    if st.button("Run Feature Selection"):
        # [Previous feature selection code remains the same]
        
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
        st.pyplot(plot_correlation_heatmap(selected_data))

if __name__ == "__main__":
    main()
