import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Global Variables (for reusability across tabs)
uploaded_file = None# A placeholder for storing the uploaded file.
df = None # A placeholder for storing the DataFrame created from the uploaded file.

# Set page layout and title
st.set_page_config(page_title="Data Explorer", layout="wide", initial_sidebar_state="expanded")

# Apply a custom style for headers and subheaders
st.markdown("""
    <style>
    .main-header {font-size: 32px; font-weight: bold; color: #2e7bcf;}
    .sub-header {font-size: 24px; font-weight: bold; color: #4a4a4a; margin-top: 10px;}
    .stApp {background-color: #f9f9f9;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for global actions
st.sidebar.header("Data Explorer App")
st.sidebar.markdown("""
    This app allows you to:
    - Upload a CSV file
    - Preprocess the data
    - Perform basic data analysis
    - Visualize the data with various plots
""")

# Main Tabs for Each Module
tabs = st.tabs(["Upload & Preprocessing", "Simple Data Analysis", "Exploratory Data Analysis (EDA)", "Visualizations"])

# Module 1: Upload & Preprocessing Tab
with tabs[0]:# Use the first tab (index 0) for the Upload & Preprocessing module.
    st.markdown('<h1 class="main-header">Upload & Preprocess Data</h1>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your CSV file", type="csv", help="Upload your dataset in CSV format.")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.markdown('<h2 class="sub-header">Preview of Uploaded Data</h2>', unsafe_allow_html=True)
        st.dataframe(df.head())
        
        # Preprocessing steps
        st.markdown('<h2 class="sub-header">Data Preprocessing Options</h2>', unsafe_allow_html=True)
        
        if st.checkbox("Show Data Types"):
            st.write(df.dtypes)
        
        if st.checkbox("Handle Missing Values"):
            st.markdown("Before handling missing values:")
            st.write(df.isnull().sum())
            
            action = st.selectbox("Choose method to handle missing values", ["Drop Rows", "Fill with Mean", "Do Nothing"])
            
            if action == "Drop Rows":
                df = df.dropna()
                st.write("After dropping missing values:")
                st.write(df.isnull().sum())
            
            elif action == "Fill with Mean":
                df = df.fillna(df.mean(numeric_only=True))
                st.write("After filling missing values:")
                st.write(df.isnull().sum())
            
            else:
                st.write("No changes made.")
        
        # Handling non-numeric columns
        st.markdown('<h2 class="sub-header">Handling Non-Numeric Columns</h2>', unsafe_allow_html=True)
        non_numeric_cols = df.select_dtypes(exclude=['number']).columns
        
        if len(non_numeric_cols) > 0:
            st.write(f"Found non-numeric columns: {list(non_numeric_cols)}")
            non_numeric_action = st.selectbox("How would you like to handle non-numeric columns?",
                                              ["Remove Non-Numeric Columns", "Attempt to Convert to Numeric", "Do Nothing"])
            
            if non_numeric_action == "Remove Non-Numeric Columns":
                df = df.drop(columns=non_numeric_cols)
                st.write("After removing non-numeric columns:")
                st.write(df.head())
            
            elif non_numeric_action == "Attempt to Convert to Numeric":
                for col in non_numeric_cols:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                st.write("After attempting conversion to numeric:")
                st.write(df.head())

# Module 2: Simple Data Analysis Tab
with tabs[1]:
    st.markdown('<h1 class="main-header">Simple Data Analysis</h1>', unsafe_allow_html=True)
    
    if df is not None:
        st.markdown('<h2 class="sub-header">Basic Data Statistics</h2>', unsafe_allow_html=True)
        st.write(df.describe())
        
        st.markdown('<h2 class="sub-header">Column-wise Analysis</h2>', unsafe_allow_html=True)
        column = st.selectbox("Select a column for analysis", df.columns)
        st.write(f"Statistics for column `{column}`:")
        st.write(df[column].describe())
        
        if st.checkbox("Show Unique Values for Categorical Columns"):
            cat_columns = df.select_dtypes(include=['object', 'category']).columns
            if len(cat_columns) > 0:
                selected_cat_col = st.selectbox("Select a categorical column", cat_columns)
                st.write(f"Unique values in `{selected_cat_col}`: {df[selected_cat_col].unique()}")
            else:
                st.write("No categorical columns found.")

# Module 3: Exploratory Data Analysis (EDA) Tab
with tabs[2]:
    st.markdown('<h1 class="main-header">Exploratory Data Analysis (EDA)</h1>', unsafe_allow_html=True)
    
    if df is not None:
        st.markdown('<h2 class="sub-header">Select Columns for Analysis</h2>', unsafe_allow_html=True)
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect("Select columns for EDA", all_columns, default=all_columns)
        
        st.markdown('<h2 class="sub-header">Select Rows for Analysis</h2>', unsafe_allow_html=True)
        row_start, row_end = st.slider("Select row range", 0, len(df), (0, len(df)))
        
        filtered_df = df.loc[row_start:row_end, selected_columns]
        st.write(f"Preview of selected data (Rows {row_start} to {row_end}):")
        st.dataframe(filtered_df.head())
        
        st.markdown('<h2 class="sub-header">Correlation Matrix</h2>', unsafe_allow_html=True)
        numeric_cols = filtered_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        if len(numeric_cols) > 1:
            st.write(f"Correlation matrix for selected numeric columns: {numeric_cols}")
            corr_matrix = filtered_df[numeric_cols].corr()
            sns.set(style="whitegrid")
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", cbar=True, linewidths=.5)
            st.pyplot(plt)
            plt.clf()
        else:
            st.write("Not enough numeric columns for a correlation matrix.")

# Module 4: Plotting Tab
with tabs[3]:
    st.markdown('<h1 class="main-header">Visualize the Data</h1>', unsafe_allow_html=True)
    
    plot_type = st.selectbox("Choose a plot type", ["Scatter Plot", "Line Plot", "Bar Plot", "Histogram"])

    st.markdown('<h2 class="sub-header">Select Columns for Plotting</h2>', unsafe_allow_html=True)
    x_axis = st.selectbox("Select X-axis", df.columns)
    y_axis = st.selectbox("Select Y-axis", df.columns)

    sns.set(style="darkgrid")
    
    if plot_type == "Scatter Plot":
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=x_axis, y=y_axis, palette="deep")
        plt.title(f'Scatter Plot: {x_axis} vs {y_axis}')
        st.pyplot(plt)
        plt.clf()

    elif plot_type == "Line Plot":
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x=x_axis, y=y_axis, palette="cool")
        plt.title(f'Line Plot: {x_axis} vs {y_axis}')
        st.pyplot(plt)
        plt.clf()

    elif plot_type == "Bar Plot":
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x=x_axis, y=y_axis, palette="muted")
        plt.title(f'Bar Plot: {x_axis} vs {y_axis}')
        st.pyplot(plt)
        plt.clf()

    elif plot_type == "Histogram":
        plt.figure(figsize=(10, 6))
        sns.histplot(df[x_axis], bins=20, color='purple')
        plt.title(f'Histogram of {x_axis}')
        st.pyplot(plt)
        plt.clf()
