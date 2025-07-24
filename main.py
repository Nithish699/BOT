import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dotenv import load_dotenv
import os

# --- Load environment variables ---
load_dotenv()

# --- Load accounts from .env ---
ACCOUNTS = []
index = 1
while True:
    email = os.getenv(f"ACCOUNT_{index}_EMAIL")
    password = os.getenv(f"ACCOUNT_{index}_PASSWORD")
    if email and password:
        ACCOUNTS.append({"email": email, "password": password})
        index += 1
    else:
        break

print(f"✅ Loaded {len(ACCOUNTS)} accounts.")
for acc in ACCOUNTS:
    print(f"Account: {acc['email']}")

# --- KodNest URLs ---
LOGIN_URL = "https://app.kodnest.com/login"
DASHBOARD_URL = "https://app.kodnest.com/my-learning/home"

# --- Simple print-based log (Render captures logs) ---
def log(message):
    print(f"[{time.ctime()}] {message}")

# --- Attendance marking function ---
def mark_attendance(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=chrome_options)

    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)

        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "login-submit-button"))).click()

        # Wait for dashboard redirect
        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))
            log(f"🔐 Login successful: {email}")
        except:
            log(f"❌ Login failed: {email}")
            driver.quit()
            return

        # Go to dashboard and mark attendance
        driver.get(DASHBOARD_URL)
        time.sleep(3)

        try:
            attendance_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mark Your Attendance')]"))
            )
            attendance_btn.click()
            log(f"✅ Attendance marked: {email}")
        except:
            log(f"❌ Attendance button not found: {email}")

    except Exception as e:
        log(f"⚠️ Error for {email}: {str(e)}")
    finally:
        driver.quit()

# --- Loop: run every 5 minutes ---
while True:
    for account in ACCOUNTS:
        mark_attendance(account["email"], account["password"])
    time.sleep(300)  # Wait 5 minutes
