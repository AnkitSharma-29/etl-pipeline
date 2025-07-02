import os, json, zipfile, io, csv, requests
from urllib.parse import urlparse, urlunparse
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator
from dotenv import load_dotenv
import google.generativeai as genai
import psycopg2
import xmltodict
load_dotenv("/opt/airflow/.env")
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

DATA_DIR = "/opt/airflow/data"
OUTPUT_CSV = os.path.join(DATA_DIR, "australian_companies.csv")
N_RESULTS = 2000
DB_PARAMS = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "postgres"
}

def get_root_url(url):
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return ''
    return urlunparse((parsed.scheme, parsed.netloc, '/', '', '', ''))

def extract_commoncrawl(**kwargs):
    """Query Common Crawl for .au domains and extract company info."""
    print("Querying Common Crawl index for .au domains...")
    api_url = "https://index.commoncrawl.org/CC-MAIN-2025-13-index?url=*.au/*&output=json"
    results = []
    try:
        for line in requests.get(api_url, stream=True, timeout=30).iter_lines():
            if line:
                data = json.loads(line)
                url = data.get('url', '')
                warc_file = data.get('filename', '')
                offset = int(data.get('offset', 0))
                length = int(data.get('length', 0))
                if url and warc_file and offset and length:
                    results.append((url, warc_file, offset, length))
                if len(results) >= N_RESULTS:
                    break
    except Exception as e:
        print(f"Error querying Common Crawl: {e}")
        return

    print(f"Found {len(results)} .au URLs. Extracting company info...")
    seen_urls = set()
    companies = []
    for idx, (url, warc_file, offset, length) in enumerate(results):
        root_url = get_root_url(url)
        if not root_url or root_url in seen_urls:
            continue
        warc_file_url = f'https://data.commoncrawl.org/{warc_file}'
        headers = {'Range': f'bytes={offset}-{offset+length-1}'}
        try:
            resp = requests.get(warc_file_url, headers=headers, stream=True, timeout=10)
            if resp.status_code != 206:
                continue
            raw_stream = io.BytesIO(resp.content)
            for record in ArchiveIterator(raw_stream):
                if record.rec_type == 'response':
                    html = record.content_stream().read()
                    try:
                        soup = BeautifulSoup(html, 'html.parser')
                    except Exception:
                        continue
                    # Company name extraction
                    og_site = soup.find('meta', property='og:site_name')
                    company_name = (og_site['content'].strip() if og_site and og_site.has_attr('content')
                                    else (soup.h1.string.strip() if soup.h1 and soup.h1.string
                                          else (soup.title.string.strip() if soup.title and soup.title.string else '')))
                    # Industry extraction
                    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
                    industry = meta_keywords['content'] if meta_keywords and meta_keywords.has_attr('content') else ''
                    # Clean fields
                    def clean(x):
                        return x.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip() if x else ''
                    root_url = clean(root_url)
                    company_name = clean(company_name)
                    industry = clean(industry)
                    # Only save if company name is not empty or generic
                    if company_name and company_name.lower() not in ['home', 'welcome', 'index']:
                        companies.append({
                            "website_url": root_url,
                            "company_name": company_name,
                            "industry": industry
                        })
                        seen_urls.add(root_url)
                    print(f"{idx+1}/{len(results)}: {root_url} | {company_name} | {industry}")
        except Exception as e:
            print(f"Error processing {warc_file_url}: {e}")
            continue

    # Ensure DATA_DIR exists
    os.makedirs(DATA_DIR, exist_ok=True)

    # Save to JSON
    json_path = os.path.join(DATA_DIR, "commoncrawl.json")
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(companies, f)
    print(f"✅ Saved {len(companies)} Common Crawl companies to {json_path}")

    # Save to CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Website URL', 'Company Name', 'Industry'])
        writer.writerows([[c['website_url'], c['company_name'], c['industry']] for c in companies])
    print(f"✅ Saved {len(companies)} records to {OUTPUT_CSV}")

#xgrokkkkkkkkkkkkk
def extract_abr_zip(**kwargs):
    """Extract ABR data from ZIP file and convert XML to JSON using streaming."""
    try:
        abr_zip_path = os.path.join(DATA_DIR, "abr.zip")
        if not os.path.exists(abr_zip_path):
            print(f"Error: {abr_zip_path} not found")
            return
        # Extract ZIP to extracted_xml
        extracted_xml_dir = os.path.join(DATA_DIR, "extracted_xml")
        with zipfile.ZipFile(abr_zip_path, "r") as zip_ref:
            zip_ref.extractall(extracted_xml_dir)
        print(f"Extracted abr.zip to {extracted_xml_dir}")

        abr_data = []
        # Process each XML file in extracted_xml
        for file in os.listdir(extracted_xml_dir):
            if file.endswith(".xml"):
                xml_path = os.path.join(extracted_xml_dir, file)
                try:
                    with open(xml_path, 'rb') as xml_file:
                        def handle_item(path, item):
                            abn = item.get('ABN')
                            name = item.get('EntityName')
                            status = item.get('EntityStatus')
                            state = item.get('State')
                            if abn and status == "Active":
                                abr_data.append({
                                    "abn": abn,
                                    "entity_name": name,
                                    "state": state
                                })
                            return True  # Continue parsing

                        # Parse with streaming
                        xmltodict.parse(xml_file, item_depth=2, item_callback=handle_item)
                    print(f"Processed XML: {xml_path}")
                except Exception as e:
                    print(f"Error parsing XML {file}: {e}")
                    continue

        # Save consolidated data to abr_data.json
        abr_json_path = os.path.join(DATA_DIR, "abr_data.json")
        try:
            with open(abr_json_path, "w", encoding='utf-8') as f:
                json.dump(abr_data, f, indent=2)
            print(f"✅ Extracted {len(abr_data)} ABR entries to {abr_json_path}")
        except Exception as e:
            print(f"Error writing to {abr_json_path}: {e}")
    except Exception as e:
        print(f"Error in ABR extraction: {e}")



def match_with_gemini(**kwargs):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent")

    with open(f"{DATA_DIR}/commoncrawl.json") as f1, open(f"{DATA_DIR}/abr_data.json") as f2:
        crawl_data = json.load(f1)
        abr_data = json.load(f2)

    matches = []
    for c in crawl_data:
        for a in abr_data:
            prompt = (
                        f"Do these refer to the same company?\n\n"
                        f"Website Company:\n"
                        f"Name: {c['company_name']}\n"
                        f"URL: {c['website_url']}\n\n"
                        f"ABR Record:\n"
                        f"Entity Name: {a['entity_name']}\n"
                        f"ABN: {a['abn']}\n\n"
                        f"Answer YES or NO. Just say 'YES' if you are confident they refer to the same company.")
            try:
                response = model.generate_content(prompt).text.strip().lower()
                if "yes" in response:
                    matches.append({
                        "abn": a['abn'],
                        "company_name": c['company_name'],
                        "website_url": c['website_url'],
                        "state": a['state']
                    })
            except Exception as e:
                print("Gemini error:", e)

    with open(f"{DATA_DIR}/matched_data.json", "w") as f:
        json.dump(matches, f)
    print(f"✅ Matched {len(matches)} entries with Gemini")

from airflow.hooks.base import BaseHook
import psycopg2
import json

def insert_to_postgres(**kwargs):
    conn = BaseHook.get_connection("aus_conntection")

    DB_PARAMS = {
        "host": "postgres",
        "port": 5432,
        "dbname": "airflow",
        "user": "airflow",
        "password": "airflow",
    }

    print("✅ DB_PARAMS:", DB_PARAMS)  # Add this line to debug

    with open(f"{DATA_DIR}/matched_data.json") as f:
        data = json.load(f)

    connection = psycopg2.connect(**DB_PARAMS)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matched_companies (
            abn TEXT PRIMARY KEY,
            company_name TEXT,
            website_url TEXT,
            state TEXT
        );
    """)
    for row in data:
        cursor.execute("""
            INSERT INTO matched_companies (abn, company_name, website_url, state)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (abn) DO NOTHING;
        """, (row["abn"], row["company_name"], row["website_url"], row["state"]))
    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Inserted into PostgreSQL")
