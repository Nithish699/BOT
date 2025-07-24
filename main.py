from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env into environment

# --- Load all accounts from env ---
ACCOUNTS = []
index = 1
while True:
    email = os.getenv(f"ACCOUNT_{index}_EMAIL")
    password = os.getenv(f"ACCOUNT_{index}_PASSWORD")
    if email and password:
        ACCOUNTS.append({"email": email, "password": password})
        index += 1
    else:
        break  # Stop if next pair not found
print(f"Loaded {len(ACCOUNTS)} accounts from environment variables.")
print("Accounts:", ACCOUNTS)
# --- URLs ---
LOGIN_URL = "https://app.kodnest.com/login"
DASHBOARD_URL = "https://app.kodnest.com/my-learning/home"

def log(message):
    print(f"[{time.ctime()}] {message}")  # Render logs output

def mark_attendance(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "login-submit-button"))).click()

        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))
            print(f"🔐 Logged in successfully as {email}.")
            log(f"Login successful: {email}")
        except:
            print(f"❌ Login failed for {email}.")
            log(f"Login failed: {email}")
            driver.quit()
            return

        driver.get(DASHBOARD_URL)
        time.sleep(3)

        try:
            attendance_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mark Your Attendance')]"))
            )
            attendance_btn.click()
            print(f"✅ Attendance marked for {email} at", time.ctime())
            log(f"Attendance marked: {email}")
        except:
            print(f"❌ Attendance button not found for {email} at", time.ctime())
            log(f"Attendance button not found: {email}")

    except Exception as e:
        print(f"⚠️ Error occurred for {email}:", e)
        log(f"Error for {email}: {str(e)}")
    finally:
        driver.quit()

# --- Run every 5 minutes ---
while True:
    for account in ACCOUNTS:
        mark_attendance(account["email"], account["password"])
    time.sleep(300)
