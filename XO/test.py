from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

driver.get("https://school-beta.edulive.net/dang-nhap")

# def get_visible_element(locator, timeout=10):
#     try:
#         return WebDriverWait(driver, timeout).until(
#             EC.visibility_of_element_located(locator)
#         )
#     except:
#         return None
def get_visible_element(locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None
def get_error_messages(driver):
    errors = driver.find_elements(By.XPATH, "//p[contains(@class,'text-red-600')]")
    return [e.text.strip() for e in errors if e.text.strip()]

# --- Case 1: Trống email + pass ---
input_email = get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']"))
input_pass = get_visible_element((By.CSS_SELECTOR, "input[type='password']"))
btn_login   = get_visible_element((By.XPATH, "//button[@type='submit']"))

input_email.send_keys("daotc@el.net")
input_pass.send_keys("123456")
btn_login.click()

messages = get_error_messages(driver)
print("⚠ Các message hiển thị:", messages)

assert any("mật khẩu" in m.lower() for m in messages)
