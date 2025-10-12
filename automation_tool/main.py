from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import uvicorn
import base64
import time
from fastapi import FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Railway!"}


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, Railway!"}


app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    url: str
    action: str

def create_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # use new headless when available
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1400,900")
    # add any other options you need
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(6)
    return driver




def create_chrome_driver():
    chrome_options = Options()
    # Run in headless mode (new headless API)
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--window-size=1400,900")

    # Explicitly tell Selenium where ChromeDriver is (from Dockerfile)
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path="/usr/bin/chromedriver"
    )
    driver.implicitly_wait(6)
    return driver

@app.post("/automate")
async def automate(task: Task):
    driver = None
    try:
        driver = create_chrome_driver()
        driver.get(task.url)
        # small wait to let JS load (tweak as needed)
        time.sleep(1)

        if task.action == "title":
            result = driver.title or ""

        elif task.action == "links":
            elements = driver.find_elements(By.TAG_NAME, "a")
            result = [el.get_attribute("href") for el in elements if el.get_attribute("href")]

        elif task.action == "text":
            body = driver.find_element(By.TAG_NAME, "body")
            text = body.text or ""
            # optionally trim extremely long text
            result = text

        elif task.action == "images":
            elements = driver.find_elements(By.TAG_NAME, "img")
            result = [el.get_attribute("src") for el in elements if el.get_attribute("src")]

        elif task.action == "screenshot":
            # return Base64 data URL so frontend can show it inline
            screenshot_b64 = driver.get_screenshot_as_base64()
            result = f"data:image/png;base64,{screenshot_b64}"

        else:
            result = f"Unknown action: {task.action}"

        return {"status": "success", "result": result}

    except Exception as e:
        return {"status": "error", "result": str(e)}

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
            
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
