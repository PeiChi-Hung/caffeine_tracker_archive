import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import re

coffee = {
    "dharkan-coffee-pods": [
        "https://www.nespresso.com/tw/zh/order/capsules/original/dharkan-coffee-pods"
    ]
}

# open chrome
service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service, options=options)

# nespresso home page
driver.get(
    "https://www.nespresso.com/tw/zh/order/capsules/original/dharkan-coffee-pods"
)

# accept cookie
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
).click()

time.sleep(3)

WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='collapse-heading-0']"))
).click()

time.sleep(5)

ingredient = driver.find_element(By.XPATH, "//*[@id='collapse-region-0']/div/p[3]")

# extract the caffeine amount
caffeine_amount = ingredient.text.splitlines()[2]
caffeine_amount = caffeine_amount.replace(" ", "")
# caffeine_amount = caffeine_amount[6::]
caffeine_amount = re.findall(r"\d+毫克/\d+毫升", caffeine_amount)[0]

print(caffeine_amount)
# translate the caffeine amount
# caffeine_amount_translated = caffeine_amount[0].replace("毫克", "mg")
# caffeine_amount_translated = caffeine_amount_translated.replace("毫升", "ml")

# add caffeine amount to corresponding coffee pod
# coffee["dharkan-coffee-pods"].append(caffeine_amount_translated)
# print(coffee)

time.sleep(10)
driver.quit()
