import pytest
import time
import sys
import os
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

# Thêm đường dẫn gốc của dự án vào sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from Pages.login_page import LoginPage
service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 15)  

def get_visible_element(driver, locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None



def login(driver):
    # driver.get("https://school-beta.edulive.net/dang-nhap")
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    print("✅ Đăng nhập thành công")

def open_class(driver):
    wait_local = WebDriverWait(driver, 15)
    class_card = wait_local.until(lambda d: get_visible_element(d, (By.CSS_SELECTOR, "a.cursor-pointer.bg-brand-50")))
    class_card.click()
    print("✅ Đã click vào lớp")

    wait_local.until(EC.url_contains("/giao-vien/quan-ly-lop-hoc/Mzg"))
    print("🎉 Đã vào trang lớp học Mzg thành công")

    # --- Kiểm tra URL ---
    assert "/quan-ly-lop-hoc/Mzg" in driver.current_url, "❌ Không vào được lớp Mzg"

@pytest.mark.usefixtures("driver")
def test_open_class(driver):
    login(driver)
    # go_to_question_bank(driver)
    open_class(driver)
    driver.quit()