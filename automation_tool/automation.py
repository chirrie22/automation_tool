# automation.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_automation(url: str, action: str):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    if action == "title":
        result = driver.title
    elif action == "links":
        links = [a.get_attribute("href") for a in driver.find_elements("tag name", "a")]
        result = links
    elif action == "screenshot":
        driver.save_screenshot("screenshot.png")
        result = "Screenshot saved as screenshot.png"
    else:
        result = "Invalid action"

    driver.quit()
    return result
