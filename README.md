# Save the formatted README.md content into a file for download

readme_final = """# ETL Pipeline: Company Data Integration using Airflow & PostgreSQL

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
