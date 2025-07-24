from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import os
from dotenv import load_dotenv

load_dotenv()

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

LOGIN_URL = "https://app.kodnest.com/login"
DASHBOARD_URL = "https://app.kodnest.com/my-learning/home"

def log(message):
    print(f"[{time.ctime()}] {message}")

def mark_attendance(email, password):
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = uc.Chrome(options=options)

        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "email"))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "login-submit-button"))).click()

        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(DASHBOARD_URL))
            log(f"✅ Logged in successfully: {email}")
        except:
            log(f"❌ Login failed for {email}")
            driver.quit()
            return

        driver.get(DASHBOARD_URL)
        time.sleep(3)

        try:
            attendance_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mark Your Attendance')]"))
            )
            attendance_btn.click()
            log(f"✅ Attendance marked for {email}")
        except:
            log(f"❌ Attendance button not found for {email}")
    except Exception as e:
        log(f"⚠️ Error for {email}: {str(e)}")
    finally:
        driver.quit()

while True:
    for account in ACCOUNTS:
        mark_attendance(account["email"], account["password"])
    time.sleep(300)
