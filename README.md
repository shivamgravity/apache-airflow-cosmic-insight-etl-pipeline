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
