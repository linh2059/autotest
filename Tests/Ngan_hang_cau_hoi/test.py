import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from Pages.login_page import LoginPage
import time

def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)

    # --- Locator chính xác cho menu 'Ngân hàng câu hỏi' ---
    menu_locator = (By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")

    # --- Chờ menu clickable ---
    menu = wait.until(EC.element_to_be_clickable(menu_locator))

    # --- Scroll để chắc chắn hiển thị ---
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)

    # --- Click bằng JS (tránh bị block) ---
    driver.execute_script("arguments[0].click();", menu)
    print("✅ Đã click menu Ngân hàng câu hỏi")

    # --- Chờ URL chuyển đúng ---
    try:
        wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    except TimeoutException:
        raise Exception(f"❌ Không chuyển sang trang Ngân hàng câu hỏi, URL hiện tại: {driver.current_url}")
    
    print(f"🎉 Đã vào trang: {driver.current_url}")

@pytest.mark.usefixtures("driver")
def test_open_question_bank(driver):
    # --- Login ---
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    # --- Click menu Ngân hàng câu hỏi ---
    go_to_question_bank(driver)
    time.sleep(2)
