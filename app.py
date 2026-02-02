import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Page Config
st.set_page_config(page_title="Cosmic Insight Dashboard", layout="wide")
st.title("☄️ Cosmic Insight: Near-Earth Object Tracker")
st.markdown("Real-time data orchestrated by **Apache Airflow** from **NASA's NeoWs API**.")

# Database Connection
@st.cache_data
def get_data():
    engine = create_engine("postgresql+psycopg2://airflow:airflow@localhost:5432/airflow")
    query = "SELECT * FROM asteroids"
    return pd.read_sql(query, engine)

try:
    df = get_data()

    if not df.empty:
        # Visualizations Section
        st.divider()
        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("🚀 Top 10 Fastest Asteroids")
            fast_df = df.sort_values('velocity_kmh', ascending=False).head(10)
            st.bar_chart(data=fast_df, x='name', y='velocity_kmh', color="#FF4B4B")

        with right_col:
            st.subheader("⚠️ Hazard Distribution")
            # Creating a Plotly pie chart for better insights
            hazard_counts = df['hazard'].value_counts().reset_index()
            hazard_counts.columns = ['Status', 'Count']
            hazard_counts['Status'] = hazard_counts['Status'].map({True: 'Hazardous', False: 'Safe'})
            
            fig = px.pie(hazard_counts, values='Count', names='Status', 
                        color='Status',
                        color_discrete_map={'Hazardous':'#FF4B4B', 'Safe':'#00CC96'},
                        hole=0.4)
            
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Ensure Docker is running and Port 5432 is exposed.")