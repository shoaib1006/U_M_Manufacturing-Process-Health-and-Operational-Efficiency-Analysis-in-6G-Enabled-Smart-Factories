# Manufacturing Process Health & Efficiency Dashboard

This project provides an analytical suite and a predictive model to monitor and evaluate the operational health of a smart factory environment.

## Project Components

1.  **thales_man.py**: A Streamlit-based web application for real-time visualization of factory metrics.
2.  **factory_efficiency_model.joblib**: A tuned Random Forest classifier that predicts machine efficiency with 99.99% accuracy.
3.  **model_predictions_for_dashboard.csv**: Exported test data used to populate the dashboard visualizations.
4.  **requirements.txt**: Python dependencies required to run the application.

## Local Setup Instructions

To run the dashboard locally, follow these steps:

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Install Dependencies
Open your terminal/command prompt and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Dashboard
In the same directory where you downloaded the files, execute:
```bash
streamlit run thales_man.py
```

## Key Insights from Analysis
*   **Efficiency Drivers**: The primary predictors of factory efficiency are **Error Rate** and **Production Speed**.
*   **Sensor Impact**: Physical sensors (Temperature, Vibration) are stable but have a lower direct correlation to categorical efficiency compared to throughput metrics.
*   **Optimization Target**: 77.8% of records fall into the 'Low' efficiency category, highlighting a significant opportunity for process refinement.