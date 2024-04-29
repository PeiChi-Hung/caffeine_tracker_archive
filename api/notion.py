import requests
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("notion_secret_key")
DATABASE_ID = os.getenv("database_id")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


# create a new page in notion data
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    return res


# check if page for a coffee pod exists
def existed(data):
    readUrl = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {"property": "Coffee Name", "title": {"contains": data}},
    }
    response = requests.request("POST", readUrl, json=payload, headers=headers)
    result = response.json()["results"]
    return len(result) == 1
