
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Smart Factory Health Dashboard', layout='wide')

st.title('🏭 Manufacturing Process Health & Efficiency Analysis')
st.markdown('This dashboard visualizes operational metrics and predictive maintenance insights for the smart factory.')

# 1. Load Data and Model
@st.cache_data
def load_data():
    df = pd.read_csv('model_predictions_for_dashboard.csv')
    return df

@st.cache_resource
def load_model():
    return joblib.load('factory_efficiency_model.joblib')

try:
    df_results = load_data()
    model = load_model()

    # 2. Sidebar Metrics
    st.sidebar.header('Factory Overview')
    total_records = len(df_results)
    avg_speed = df_results['Production_Speed_units_per_hr'].mean()
    
    st.sidebar.metric("Total Samples", f"{total_records:,}")
    st.sidebar.metric("Avg Production Speed", f"{avg_speed:.2f} u/hr")

    # 3. Layout - Row 1: Efficiency Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Actual Efficiency Distribution')
        fig_bar = plt.figure(figsize=(8, 5))
        sns.countplot(x='Actual_Efficiency', data=df_results, order=['Low', 'Medium', 'High'], palette='viridis')
        st.pyplot(fig_bar)

    with col2:
        st.subheader('Predicted vs Actual Match')
        correct_preds = (df_results['Actual_Efficiency'] == df_results['Predicted_Efficiency']).sum()
        accuracy = correct_preds / total_records
        st.write(f'Model Accuracy on Test Set: **{accuracy*100:.2f}%**')
        st.info('Note: The perfect accuracy reflects strict KPI-based labeling.')

    # 4. Row 2: Operational Deep Dive
    st.divider()
    st.subheader('Sensor Analysis')
    sensor_to_plot = st.selectbox('Select Metric to Visualize:', ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW', 'Error_Rate_%'])
    
    fig_box = plt.figure(figsize=(10, 5))
    sns.boxplot(x='Actual_Efficiency', y=sensor_to_plot, data=df_results, order=['Low', 'Medium', 'High'])
    st.pyplot(fig_box)

    # 5. Raw Data Preview
    if st.checkbox('Show Raw Prediction Data'):
        st.dataframe(df_results.head(100))

except FileNotFoundError:
    st.error('Required files not found. Please ensure factory_efficiency_model.joblib and model_predictions_for_dashboard.csv are in the same folder.')
