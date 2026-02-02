import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

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
        # Metrics Row
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Objects Tracked", len(df))
        col2.metric("Hazardous Objects", len(df[df['hazard'] == True]))
        col3.metric("Avg Velocity (km/h)", f"{int(df['velocity_kmh'].mean()):,}")

        # Visualizations
        st.divider()
        left_col, right_col = st.columns(2)

        with left_col:
            st.subheader("Top 10 Fastest Asteroids")
            fast_df = df.sort_values('velocity_kmh', ascending=False).head(10)
            st.bar_chart(data=fast_df, x='name', y='velocity_kmh', color="#FF4B4B")

        with right_col:
            st.subheader("Hazard Distribution")
            hazard_counts = df['hazard'].value_counts()
            st.pie_chart(hazard_counts)

        st.subheader("Raw Data Inspection")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Database is connected but the 'asteroids' table is empty. Please run your Airflow DAG.")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Ensure Docker is running and Port 5432 is exposed.")