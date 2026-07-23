from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)
try:
    # Home page login form is reachable over HTTP (req 1)
    driver.get("http://localhost:5000/")
    driver.find_element(By.NAME, "username")
    driver.find_element(By.NAME, "password")

    # Create an account through the UI with a compliant password -> Welcome (req 6, 8)
    driver.get("http://localhost:5000/register")
    driver.find_element(By.NAME, "username").send_keys("ui_user")
    driver.find_element(By.NAME, "password").send_keys("Selenium-UI-Pass-1!")
    driver.find_element(By.TAG_NAME, "button").click()
    assert "Welcome" in driver.page_source

    print("UI tests passed")
finally:
    driver.quit()
