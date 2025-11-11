import yaml
import time
import datetime
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

DEBUG_INTERVAL = 10  # 10 secondes au lieu de minutes

def load_schedule(path="schedule.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)["schedule"]

def get_current_block(schedule):
    now = datetime.datetime.now().time()
    for block in schedule:
        start = datetime.datetime.strptime(block["start"], "%H:%M").time()
        end = datetime.datetime.strptime(block["end"], "%H:%M").time()
        if start <= now or (start > end and (now >= start or now <= end)):
            if start <= now <= end or (start > end and (now >= start or now <= end)):
                return block
    return None

def open_urls(urls, interval, driver):
    for url in urls:
        print(f"Opening {url}")
        driver.get(url)
        time.sleep(DEBUG_INTERVAL or interval * 60)

def main():
    schedule = load_schedule()

    chrome_options = Options()
    chrome_options.add_argument("--start-fullscreen")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        while True:
            block = get_current_block(schedule)
            if block:
                print(f"Current block: {block['name']}")
                open_urls(block["urls"], block["interval"], driver)
            else:
                print("No matching schedule block. Sleeping...")
                time.sleep(DEBUG_INTERVAL or 60)
    except KeyboardInterrupt:
        driver.quit()

if __name__ == "__main__":
    main()
