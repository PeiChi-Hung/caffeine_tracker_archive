import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

# open chrome
service = Service(executable_path="chromedriver.exe")
options = webdriver.ChromeOptions()

options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service, options=options)

# nespresso home page
driver.get("https://www.nespresso.com/tw/zh/order/capsules/original/")

# accept cookie
WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
).click()

time.sleep(5)

tracking_lists = [
    "限量推薦",
    "義式致敬經典系列",
    "咖啡大師特調系列",
    "環遊世界咖啡系列",
    "單一產區咖啡系列",
    "濃縮咖啡系列",
]


# get link for each item in the limited offer
for lst in tracking_lists:
    item_count = limited_counts = len(
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
        tracking_position += 1


driver.quit()
