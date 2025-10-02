import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture(scope="function")
def driver():
    service = Service(r"C:\Users\admin\Documents\Selenium\School_teacher\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_debug_page(driver):
    URL = "https://school-beta.edulive.net/dang-nhap"
    driver.get(URL)
    
    # Đợi trang load
    time.sleep(3)
    
    # In ra tất cả input elements
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"🔍 Tìm thấy {len(inputs)} input elements:")
    for i, inp in enumerate(inputs):
        print(f"  {i+1}. Type: {inp.get_attribute('type')}, Placeholder: {inp.get_attribute('placeholder')}, Name: {inp.get_attribute('name')}")
    
    # In ra tất cả button elements
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"🔍 Tìm thấy {len(buttons)} button elements:")
    for i, btn in enumerate(buttons):
        print(f"  {i+1}. Text: {btn.text}, Class: {btn.get_attribute('class')}")
    
    # Thử tìm input theo các cách khác nhau
    print("\n🔍 Thử tìm input username:")
    selectors = [
        "input[placeholder*='username']",
        "input[placeholder*='email']", 
        "input[placeholder*='tên']",
        "input[type='email']",
        "input[name*='email']",
        "input[name*='username']"
    ]
    
    for selector in selectors:
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"  ✅ Tìm thấy với selector: {selector}")
            print(f"     - Type: {element.get_attribute('type')}")
            print(f"     - Placeholder: {element.get_attribute('placeholder')}")
            print(f"     - Name: {element.get_attribute('name')}")
            break
        except:
            print(f"  ❌ Không tìm thấy với selector: {selector}")
    
    # Thử tìm button đăng nhập
    print("\n🔍 Thử tìm button đăng nhập:")
    button_selectors = [
        "//button[contains(text(),'Đăng nhập')]",
        "//button[contains(text(),'Login')]",
        "//button[contains(text(),'Sign in')]",
        "//input[@type='submit']",
        "//button[@type='submit']"
    ]
    
    for selector in button_selectors:
        try:
            element = driver.find_element(By.XPATH, selector)
            print(f"  ✅ Tìm thấy button với selector: {selector}")
            print(f"     - Text: {element.text}")
            print(f"     - Type: {element.get_attribute('type')}")
            break
        except:
            print(f"  ❌ Không tìm thấy button với selector: {selector}")
    
    # Đợi để có thể xem kết quả
    time.sleep(5)

