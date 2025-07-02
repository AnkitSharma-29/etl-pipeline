# 🏗️ Company Data ETL Pipeline (Airflow + Docker)

This repository contains a **complete end-to-end ETL pipeline** built using **Python**, **Dockerized Apache Airflow**, and **PostgreSQL**. It extracts company data from CommonCrawl and ABR datasets, uses **Google's Gemini API** for entity matching, and stores the matched results into a PostgreSQL database.

---

## ✅ Project Status: Completed

- ✅ `commoncrawl_extract.py` extracts companies in JSON format  
- ✅ `abr_extract.py` extracts ABR ZIP to XML and parses data  
- ✅ Gemini-based entity matching completed  
- ✅ Matched data inserted into PostgreSQL  
- ✅ DAGs running successfully in Airflow  

---

## 📦 Features

- 🔍 Extract `.au` domain company info from **CommonCrawl**
- 📄 Extract **ABN registry data** from zipped XML (ABR)
- 🧠 **Match company entries** using **Gemini LLM**
- 💾 **Load matched data** into **PostgreSQL**
- 🔁 **Orchestration with Apache Airflow** in Dockerized environment

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

```
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

| Component        | Technology                   |
|------------------|------------------------------|
| Orchestration     | Apache Airflow (Docker)      |
| Extraction        | Python + Requests + Warcio   |
| Parsing           | BeautifulSoup + xmltodict    |
| AI Matching       | Google Gemini API            |
| Storage           | PostgreSQL                   |
| IDE               | Visual Studio Code           |

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/etl-pipeline.git
cd etl-pipeline
```

### 2. Configure Environment

Create a `.env` file with your PostgreSQL credentials and Gemini API key.

### 3. Start Docker

```bash
docker-compose up --build -d
```

### 4. Initialize Airflow DB

```bash
docker-compose run --rm airflow-webserver airflow db init
```

### 5. Create Airflow Admin User

```bash
docker-compose run --rm airflow-webserver airflow users create \
  --username admin --password admin --role Admin \
  --firstname Admin --lastname User --email admin@example.com
```

### 6. Access Airflow UI

Visit: [http://localhost:8080](http://localhost:8080)  
Login: `admin` / `admin`

---

## 🤖 Matching Prompt (Gemini)

```text
Do these refer to the same company?  
Website: {company_name} ({url})  
ABR: {entity_name} ({abn})  
Answer YES or NO.
```
![Screenshot 2025-07-03 001914](https://github.com/user-attachments/assets/7d66cda7-0b0c-4902-9ffb-b87182623901)
![Screenshot 2025-07-03 001453](https://github.com/user-attachments/assets/99d321b9-04ec-4c66-bbfd-21f52394095c)
![Screenshot 2025-07-02 114937](https://github.com/user-attachments/assets/b85c45e1-efb2-4aa3-9e20-24b03048d560)
![Screenshot 2025-07-02 114744](https://github.com/user-attachments/assets/4975f5d4-fcd4-47d3-8926-f8af77cd1a82)

---

## 📌 Contact

📧 Email: [csvtustudent@gmail.com](mailto:csvtustudent@gmail.com)  
👨‍💻 Developed by **Ankit Sharma**
