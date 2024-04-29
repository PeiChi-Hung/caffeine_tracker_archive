import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from collections import defaultdict
import re
from api.notion import *


# open chrome
service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=service, options=options)

# nespresso home page
driver.get("https://www.nespresso.com/tw/zh/order/capsules/original/")

# accept cookie
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
).click()

time.sleep(5)

tracking_lists = [
    "限量推薦",  # Limited Edition and Seasonal
    # "義式致敬經典系列",  # Ispirazione Italiana
    # "咖啡大師特調系列",  # Barista Creations
    # "環遊世界咖啡系列",  # Master Origins
    # "單一產區咖啡系列",  # World Explorations
    # "濃縮咖啡系列",  # The Original Collection
]

coffee_dict = defaultdict(list)  # coffee pod: [coffee_pod, url, caffeine_amount]
# get link for each item in tracking list

for lst in tracking_lists:
    item_count = len(
        driver.find_elements(By.XPATH, "//nb-sku-coffee[@tracking_list='" + lst + "']")
    )
    tracking_position = 1
    while tracking_position <= item_count:
        limited_item = driver.find_element(
            By.XPATH,
            "//nb-sku-coffee[@tracking_list='"
            + lst
            + "'][@tracking_position ="
            + str(tracking_position)
            + "]/div/a",
        )
        url = limited_item.get_attribute("href")
        coffee_pod = urlparse(url).path.split("/")[-1]
        # avoid adding package to the dictionary
        if "pack" not in coffee_pod:
            coffee_dict[coffee_pod].append(coffee_pod)
            coffee_dict[coffee_pod].append(url)
        tracking_position += 1

print("Finish scripting coffee name and url")
print(coffee_dict)
try:
    for coffee in coffee_dict:
        driver.get(coffee_dict[coffee][1])

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='collapse-heading-0']"))
        ).click()

        time.sleep(5)

        ingredient = driver.find_element(
            By.XPATH, "//*[@id='collapse-region-0']/div/p[3]"
        )

        # extract the caffeine amount
        caffeine_amount = ingredient.text.splitlines()[2]
        caffeine_amount = caffeine_amount.replace(" ", "")
        caffeine_amount = re.findall(r"\d+毫克/\d+毫升", caffeine_amount)[0]

        # translate the caffeine amount
        caffeine_amount_translated = caffeine_amount.replace("毫克", "mg")
        caffeine_amount_translated = caffeine_amount_translated.replace("毫升", "ml")
        # add caffeine amount to corresponding coffee pod
        coffee_dict[coffee].append(caffeine_amount_translated)
        print(coffee_dict)
        # post data to notion database
        data = {
            "Coffee Name": {"title": [{"text": {"content": coffee_dict[coffee][0]}}]},
            "URL": {"url": coffee_dict[coffee][1]},
            "Caffeine Amount": {
                "rich_text": [{"text": {"content": coffee_dict[coffee][2]}}]
            },
        }
        if not existed(coffee):
            create_page(data)

except ConnectionRefusedError:
    print("Machine refused to connect")

driver.quit()
