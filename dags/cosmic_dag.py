from airflow.decorators import dag, task
from datetime import datetime
import requests
import pandas as pd

@dag(
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=['space_weather', 'etl']
)
def cosmic_insight_pipeline():

    @task
    def extract_neo_data():
        # Using NASA's demo key for the POC
        url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2026-01-30&api_key=DEMO_KEY"
        response = requests.get(url).json()
        return response['near_earth_objects']

    @task
    def transform_data(raw_data):
        all_objects = []
        for date in raw_data:
            for obj in raw_data[date]:
                all_objects.append({
                    'id': obj['id'],
                    'name': obj['name'],
                    'hazard': obj['is_potentially_hazardous_asteroid'],
                    'velocity_kmh': obj['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
                })
        df = pd.DataFrame(all_objects)
        return df.to_json()

    @task
    def load_to_postgres(json_data):
        df = pd.read_json(json_data)
        # In a real setup, use PostgresHook here
        print(f"Loading {len(df)} asteroids into the warehouse...")

    # Define dependencies
    raw = extract_neo_data()
    clean = transform_data(raw)
    load_to_postgres(clean)

cosmic_insight_pipeline()