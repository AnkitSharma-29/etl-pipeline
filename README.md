# 🏗️ Company Data ETL Pipeline (Airflow + Docker)

This repository contains an end-to-end ETL pipeline built using **Python**, **Dockerized Apache Airflow**, and **PostgreSQL**. It extracts company data from CommonCrawl and ABR datasets, uses Google's **Gemini API** for entity matching, and stores the matched results into a PostgreSQL database.

> 🚧 **Status:** In development phase  
> ✅ `commoncrawl_extract.py` is working and extracting companies in JSON format  
> ✅ `abr_extract.py` extracts ABR ZIP to XML and parses data correctly  
> ❗ Currently troubleshooting **DAGs stuck in "queued" state** due to Airflow-Docker performance issues

---

## 📦 Features

- Extract `.au` domain company info from **CommonCrawl**
- Extract **ABN registry** data from zipped **XML (ABR)**
- Match entries using **Gemini LLM**
- Load matched data into **PostgreSQL**
- Orchestrated using **Airflow in Docker**

---

## 🐍 Main Python Libraries Used

```python
import os, json, zipfile, io, csv, requests
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator
import xmltodict
import google.generativeai as genai
import psycopg2
```

---

## 🌀 Airflow DAG Flow

```text
Extract from CommonCrawl (.au)
        ↓
Extract from ABR XML (.zip)
        ↓
Match using Gemini LLM
        ↓
Load matched companies to PostgreSQL
```

---

## 📁 Folder Structure

```
etl_start/
├── dags/
│   └── company_data_etl.py         # Airflow DAG
├── config/scripts/pipeline_utils.py# Main ETL logic
├── data/                           # Output JSON, CSV
├── docker-compose.yaml
├── .env
└── requirements.txt
```

---

## ⚙️ Technologies Used

| Component     | Technology                  |
|---------------|-----------------------------|
| Orchestration | Apache Airflow (Docker)     |
| Extraction    | Python + Requests + Warcio  |
| Parsing       | BeautifulSoup + xmltodict   |
| AI Matching   | Google Gemini API           |
| Storage       | PostgreSQL                  |
| IDE           | Visual Studio Code          |

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline
```

2. **Configure Environment**
Create a `.env` file with your PostgreSQL and Gemini API key.

3. **Start Docker**
```bash
docker-compose up --build -d
```

4. **Initialize Airflow**
```bash
docker-compose run --rm airflow-webserver airflow db init
```

5. **Create Airflow Admin User**
```bash
docker-compose run --rm airflow-webserver airflow users create \
  --username admin --password admin --role Admin \
  --firstname Admin --lastname User --email admin@example.com
```

6. **Visit Airflow UI**
- http://localhost:8080  
- Login: `admin` / `admin`

---

## ✅ Current Progress

- [x] CommonCrawl JSON extraction
- [x] ABR zip to XML + JSON extraction
- [x] Gemini-based matching
- [x] Insert into PostgreSQL
- [ ] DAG stuck in queued state (performance debugging)

---

## 🤖 Matching Prompt (Gemini)

```text
Do these refer to the same company?
Website: {company_name} ({url})
ABR: {entity_name} ({abn})
Answer YES or NO.
```

---

## 📌 Contact

For any issues, feel free to open an issue on the GitHub repository or reach out.

---

> Developed by Ankit Sharma 💻
