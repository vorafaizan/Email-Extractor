# # from flask import Flask, render_template, request
# # import os
# # import pickle
# # import re
# # import time
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from bs4 import BeautifulSoup
# #
# # app = Flask(__name__)
# # COOKIES_FILE = "linkedin_cookies.pkl"
# #
# #
# #
# # def start_driver():
# #     options = webdriver.ChromeOptions()
# #     options.add_argument("--start-maximized")
# #     options.add_argument("--disable-blink-features=AutomationControlled")
# #     options.add_argument("--headless")  # Run Chrome in headless mode
# #     options.add_argument("--disable-gpu")  # Disable GPU acceleration
# #     driver = webdriver.Chrome(options=options)
# #     return driver
# #
# # @app.route('/', methods=['GET', 'POST'])
# # def index():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         post_url = request.form['post_url']
# #
# #         emails = scrape_linkedin(username, password, post_url)
# #         return render_template('results.html', emails=emails)
# #
# #     return render_template('index.html')
# #
# # def scrape_linkedin(username, password, post_url):
# #     driver = start_driver()
# #     driver.get("https://www.linkedin.com/")
# #     time.sleep(5)
# #
# #     if os.path.exists(COOKIES_FILE) and os.path.getsize(COOKIES_FILE) > 0:
# #         try:
# #             with open(COOKIES_FILE, "rb") as file:
# #                 cookies = pickle.load(file)
# #                 for cookie in cookies:
# #                     driver.add_cookie(cookie)
# #             driver.refresh()
# #             time.sleep(5)
# #         except Exception:
# #             print("⚠️ Cookie file corrupted, logging in fresh.")
# #
# #     if "feed" not in driver.current_url:
# #         driver.get("https://www.linkedin.com/login")
# #         time.sleep(5)
# #         driver.find_element(By.ID, "username").send_keys(username)
# #         driver.find_element(By.ID, "password").send_keys(password)
# #         driver.find_element(By.XPATH, '//button[@type="submit"]').click()
# #         time.sleep(5)
# #
# #         with open(COOKIES_FILE, "wb") as file:
# #             pickle.dump(driver.get_cookies(), file)
# #
# #     driver.get(post_url)
# #     time.sleep(5)
# #
# #     while True:
# #         try:
# #             load_more_button = WebDriverWait(driver, 10).until(
# #                 EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Load more comments']"))
# #             )
# #             driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
# #             load_more_button.click()
# #             time.sleep(3)
# #         except Exception:
# #             break
# #
# #     html_source = driver.page_source
# #     soup = BeautifulSoup(html_source, 'html.parser')
# #     comments_section = soup.get_text()
# #     email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
# #     emails = sorted(set(re.findall(email_pattern, comments_section)))
# #
# #     driver.quit()
# #     return emails
# #
# # if __name__ == '__main__':
# #     app.run(debug=True)
#
# from flask import Flask, render_template, request
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import re
#
# app = Flask(__name__)
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         post_url = request.form['post_url']
#         emails = scrape_linkedin(username, password, post_url)
#         return render_template('results.html', emails=emails)
#     return render_template('index.html')
#
# def scrape_linkedin(username, password, post_url):
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome(options=options)
#
#     try:
#         driver.get("https://www.linkedin.com/login")
#
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
#
#         driver.find_element(By.ID, "username").send_keys(username)
#         driver.find_element(By.ID, "password").send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#
#         WebDriverWait(driver, 10).until(EC.url_contains("feed"))
#         print("✅ Login successful")
#
#         driver.get(post_url)
#
#         while True:
#             try:
#                 load_more = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Load more comments')]")))
#                 driver.execute_script("arguments[0].scrollIntoView(true);", load_more)
#                 load_more.click()
#                 print("📝 Clicked 'Load more comments'")
#             except TimeoutException:
#                 print("✅ All comments loaded")
#                 break
#
#         comments = driver.find_elements(By.XPATH, "//span[contains(@class, 'comment')]")
#         emails = set()
#         email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
#         for comment in comments:
#             email_matches = re.findall(email_pattern, comment.text)
#             emails.update(email_matches)
#
#         return sorted(emails)
#
#     except TimeoutException:
#         print("❌ Timeout while waiting for page elements")
#
#     except NoSuchElementException as e:
#         print(f"❌ Element not found: {e}")
#
#     finally:
#         driver.quit()
#
# if __name__ == '__main__':
#     app.run(debug=True)


#
# from flask import Flask, render_template, request
# from load_more import extract_clean_emails
#
# app = Flask(__name__)
#
#
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     emails = None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         post_url = request.form['post_url']
#         emails = extract_clean_emails(username, password, post_url)
#         return render_template('results.html', emails=emails)
#
#     return render_template('index.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, request
from load_more import extract_clean_emails

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    emails = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        post_url = request.form['post_url']
        emails = extract_clean_emails(username, password, post_url)
        return render_template('results.html', emails=emails)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
