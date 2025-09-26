import pytest
import pyautogui
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

def close_chrome_password_popup():
    # chờ popup hiện (tuỳ máy bạn, có thể 2-3s sau login)
    time.sleep(2)
    pyautogui.press("enter")   # giả lập Enter để đóng popup

def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    # demo_pause() 
    print("✅ Vào trang Ngân hàng câu hỏi")


@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    close_chrome_password_popup()
    # go_to_question_bank(driver)
    time.sleep(10)
    driver.quit()
    # document.querySelectorAll("input[type=file]")
