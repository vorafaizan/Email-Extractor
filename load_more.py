import time
import pickle
import os
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Path for saved cookies
COOKIES_FILE = "linkedin_cookies11.pkl"

# Function to extract emails from LinkedIn post
def extract_clean_emails(username, password, post_url):
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.linkedin.com/")
        time.sleep(5)

        # Load cookies if available
        if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
            with open(COOKIES_FILE, "rb") as file:
                try:
                    cookies = pickle.load(file)
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                    driver.refresh()
                    time.sleep(5)
                except EOFError:
                    print("⚠️ Cookie file is empty or corrupted, logging in fresh.")
        else:
            print("⚠️ No valid cookies found, logging in fresh.")

        if "feed" not in driver.current_url:
            driver.get("https://www.linkedin.com/login")
            time.sleep(5)

            driver.find_element(By.ID, "username").send_keys(username)
            time.sleep(2)
            driver.find_element(By.ID, "password").send_keys(password)
            time.sleep(2)
            driver.find_element(By.XPATH, '//button[@type="submit"]').click()
            time.sleep(5)

            with open(COOKIES_FILE, "wb") as file:
                pickle.dump(driver.get_cookies(), file)

        driver.get(post_url)
        time.sleep(5)

        # Click 'Load more comments' button until all comments load
        while True:
            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Load more comments']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                time.sleep(2)
                load_more_button.click()
                print("📝 Clicked 'Load more comments'")
                time.sleep(3)
            except Exception:
                print("✅ All comments loaded or button not found")
                break

        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        comments_section = soup.get_text()
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        emails = re.findall(email_pattern, comments_section)
        unique_emails = sorted(set(emails))

        if unique_emails:
            with open('linkedin_emails.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Email'])
                for email in unique_emails:
                    writer.writerow([email])

        return unique_emails

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return []

    finally:
        driver.quit()
