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


def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    print(res.status_code)
    return res


# dummy data
# coffee_name = "dharkan-coffee-pods"
# url = "https://www.nespresso.com/tw/zh/order/capsules/original/dharkan-coffee-pods"
# caffeine_amount = "75mg/25ml"
