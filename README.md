# Cosmic Insight: NASA NEO ETL Pipeline
### A Proof of Concept (POC) Data Pipeline built with Apache Airflow

## 1. Project Overview
**Cosmic Insight** is an automated ETL (Extract, Transform, Load) pipeline designed to track Near-Earth Objects (NEOs) using NASA's Open APIs. This project demonstrates how to orchestrate a data workflow that handles external API consumption, data cleaning with Python, and structured storage in a Relational Database (PostgreSQL).

### Key Features
* **Automated Extraction:** Fetches daily asteroid data from NASA’s NeoWs API.
* **Data Transformation:** Filters objects based on hazard status and converts velocity metrics.
* **Reliable Loading:** Ensures data integrity using Airflow's Idempotency principles.
* **Containerized Environment:** Fully managed via Docker for consistent deployment.

---

## 2. Solution Architecture
The pipeline follows a **Medallion (Bronze-Silver-Gold)** data architecture:

1.  **Extract (Bronze):** The pipeline calls the NASA API and retrieves raw JSON data.
2.  **Transform (Silver):** Data is parsed using Pandas. We filter for critical fields: `name`, `is_potentially_hazardous`, and `close_approach_data`.
3.  **Load (Gold):** The cleaned, structured data is upserted into a PostgreSQL "Data Warehouse" table for analytical use.

---

## 3. Tech Stack
* **Orchestrator:** Apache Airflow 2.7.1
* **Language:** Python 3.10
* **Database:** PostgreSQL 13
* **Infrastructure:** Docker & Docker Compose
* **Libraries:** Pandas, Requests, SQLAlchemy

---

## 4. Project Structure
```text
.
├── dags/
│   └── cosmic_dag.py         # The Airflow DAG definition
├── logs/                     # Airflow execution logs (Auto-generated)
├── plugins/                  # Custom Airflow plugins (Optional)
├── docker-compose.yaml       # Container orchestration file
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 5. Setup And Installation
### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* NASA API Key

### Step-by-Step Deployment
#### 1. Clone the repository
```bash
git clone https://github.com/shivamgravity/apache-airflow-cosmic-insight-etl-pipeline
cd apache-airflow-cosmic-insight-etl-pipeline
```

#### 2. Initialize Environment
Create the necessary direcotories and set the user ID to avoid permission issues.
```bash
mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

#### 3. Initialize the Database
```bash
docker-compose up airflow-init
```

#### 4. Launch the Pipeline
```bash
docker-compose up -d
```

## 6. How to Use
1. **Access the UI:** Open [http://localhost:8080](http://localhost:8080) in your browser.
2. **Login:** Use username `airflow` and password `airflow`.
3. **Activate DAG:** Locate `cosmic_insight_pipeline` in the DAGs list and toggle the "Unpause" switch.
4. **Trigger:** Click the "Play" button on the right to manually trigger a run.
5. **Monitor:** Check the "Graph" view to see the tasks execute in real-time.
