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
driver.get("https://www.nespresso.com/au/en/order/capsules/original")

time.sleep(5)

tracking_lists = [
    "Limited Edition and Seasonal",
    # "Ispirazione Italiana",
    # "Barista Creations",
    # "Master Origins",
    # "World Explorations",
    # "The Original Collection",
]

coffee_dict = defaultdict(list)  # coffee pod: [coffee_pod, url, caffeine_amount]

# get price for each item in tracking list
for lst in tracking_lists:
    item_count = len(
        driver.find_elements(By.XPATH, "//nb-sku-coffee[@tracking_list='" + lst + "']")
    )
    tracking_position = 1
    while tracking_position <= item_count:
        item = driver.find_element(
            By.XPATH,
            "//nb-sku-coffee[@tracking_list='"
            + lst
            + "'][@tracking_position ="
            + str(tracking_position)
            + "]/div/a",
        )
        url = item.get_attribute("href")
        coffee_pod = urlparse(url).path.split("/")[-1]
        price = driver.find_element(
            By.XPATH,
            "//nb-sku-coffee[@tracking_list='"
            + lst
            + "'][@tracking_position ="
            + str(tracking_position)
            + "]/div[2]/div/div/p[2]",
        )
        capsule_price = re.findall("\d+\.?\d*", price.text)[0]
        # avoid adding package to the dictionary
        if "pack" not in coffee_pod:
            coffee_dict[coffee_pod].append(coffee_pod)
            coffee_dict[coffee_pod].append(float(capsule_price))

        if get_page(coffee_pod) != "Not Found":
            # add price to the database
            page_id = get_page(coffee_pod)
            add_price(page_id, float(capsule_price))
        else:
            print(coffee_pod)
        tracking_position += 1
print(coffee_dict)
