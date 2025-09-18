from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://school-beta.edulive.net/dang-nhap")
# print(driver.page_source) 
wait = WebDriverWait(driver, 15)

# --- Input Username ---
def get_visible_element(locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None

# --- Input Username ---
username_input = wait.until(lambda d: get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']")))
username_input.send_keys("daotc@el.net")

# --- Input Password ---
password_input = wait.until(lambda d: get_visible_element((By.CSS_SELECTOR, "input[type='password']")))
password_input.send_keys("123456")
# --- Checkbox "Nhớ mật khẩu" ---
remember_button = wait.until(lambda d: get_visible_element(
    (By.XPATH, "//button[.//p[contains(text(),'Ghi nhớ đăng nhập')]]")
))
driver.execute_script("arguments[0].click();", remember_button)  # click an toàn bằng JS

# --- Click "Đăng nhập" ---
login_button = wait.until(lambda d: get_visible_element(
    (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
))
login_button.click()

print("✅ Test login modal chạy xong!")
time.sleep(2)
driver.quit()
