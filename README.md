# ETL Pipeline: Company Data Integration using Airflow & PostgreSQL

This repository contains a basic ETL (Extract, Transform, Load) pipeline project designed to extract company data, transform and clean it, and load it into a PostgreSQL database. The orchestration is handled by Apache Airflow running in a Docker environment. Entity matching will later be implemented using a Large Language Model (LLM).

---

## 🗃️ Dataset

The dataset for this project will include company details extracted from various sources (CSV, API, etc.). It is currently being prepared and stored in the `/data/` directory.

---

## 🛠 Installation & Setup

To run this project locally using Docker and Airflow:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/etl-pipeline.git
   cd etl-pipeline
   ```

2. Start Airflow and other services:
   ```bash
   docker-compose up --build -d
   ```

3. Initialize Airflow:
   ```bash
   docker-compose run --rm airflow-webserver airflow db init
   ```

4. Create Airflow Admin user:
   ```bash
   docker-compose run --rm airflow-webserver airflow users create \\
     --username admin --password admin --role Admin \\
     --firstname Admin --lastname User --email admin@example.com
   ```

5. Access the Airflow web UI at: [http://localhost:8080](http://localhost:8080)  
   - Login with:  
     **Username**: `admin`  
     **Password**: `admin`

---

## 📁 Project Structure

```
etl_start/
├── config/              # Configuration files
├── dags/                # Airflow DAGs
├── data/                # Raw/processed data
├── logs/                # Airflow logs
├── plugins/             # Airflow plugins (if needed)
├── venv/                # Local virtual environment (optional)
├── .env                 # Environment variables
├── docker-compose.yaml  # Docker service definitions
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 🔄 ETL Flow

- **Extract**: Pull company data from static files or APIs.
- **Transform**: Clean and normalize data (in progress).
- **Load**: Insert into PostgreSQL database.
- **Match**: Use LLM (e.g., Gemini or OpenAI) for fuzzy entity matching (planned).

---

## 💡 Technologies Used

- **Apache Airflow** – Workflow orchestration
- **Docker** – Environment setup
- **Python** – Data processing scripts
- **PostgreSQL** – Target database
- **LLM (Planned)** – Entity resolution/matching
- **dbt (Planned)** – Transformations and testing

---

## 🧪 Known Issues

- DAGs may get stuck in a "queued" state (scheduler debugging in progress).
- Entity matching and dbt models are planned but not yet implemented.

---

## ✨ Future Improvements

- Integrate LLM-based fuzzy matching (e.g., OpenAI or Gemini)
- Add dbt for transformations and testing
- Automate DAG triggers via external API
- Deploy on cloud (optional)

---

## 💻 Development Environment

- **IDE Used**: Visual Studio Code
- **Recommended Extensions**: Python, Docker, Airflow, dbt

---

## 📌 Note

This project is currently under development and is submitted as part of an assessment. Some components are partially implemented or pending.
