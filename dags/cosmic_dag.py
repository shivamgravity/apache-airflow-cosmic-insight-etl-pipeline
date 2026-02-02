from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
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
        import requests
        # Using a dynamic date to ensure we always have data for "today"
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&api_key=DEMO_KEY"
        
        response = requests.get(url)
        data = response.json()
        
        # Check if the key exists before accessing it
        if 'near_earth_objects' not in data:
            error_msg = data.get('error_message', 'Unknown API Error')
            raise ValueError(f"NASA API Error: {error_msg}")
            
        return data['near_earth_objects']

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
        import pandas as pd
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        
        # 1. Convert the JSON back to a DataFrame
        df = pd.read_json(json_data)
        
        # 2. Use the PostgresHook to get the connection we just saved in the UI
        pg_hook = PostgresHook(postgres_conn_id='postgres_default')
        engine = pg_hook.get_sqlalchemy_engine()
        
        # 3. Use 'replace' to ensure the DAG never fails on duplicate IDs
        # This is perfect for a POC demo to ensure a smooth video recording.
        df.to_sql('asteroids', engine, if_exists='replace', index=False)
        
        print(f"Successfully loaded {len(df)} records into the Gold Layer.")

    # Define dependencies
    raw = extract_neo_data()
    clean = transform_data(raw)
    load_to_postgres(clean)

cosmic_insight_pipeline()