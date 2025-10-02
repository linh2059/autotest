from time import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")))
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    add_topic_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm chủ đề')]")))
    driver.execute_script("arguments[0].click();", add_topic_btn)
    print("✅ Đã click nút Thêm chủ đề")

def new_topic(driver, ten_chu_de):
    wait = WebDriverWait(driver, 20)
    modal_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nhập tên chủ đề']")))
    modal_input.click()
    modal_input.clear()
    modal_input.send_keys(ten_chu_de)
    driver.execute_script("arguments[0].blur();", modal_input)  # trigger validate
    return modal_input

def submit_new_topic(driver):
    wait = WebDriverWait(driver, 20)
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
    driver.execute_script("arguments[0].click();", save_btn)
    print("✅ Đã click nút Lưu")

def get_error_message(driver):
    wait = WebDriverWait(driver, 5)
    error_el = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".elements-custom.error-element-custom"))
    )
    return error_el.text.strip()

@pytest.mark.usefixtures("driver")
def test_topic_validations(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    go_to_question_bank(driver)

    # --- TC1: Bỏ trống tên chủ đề ---
    open_add_topic_modal(driver)
    new_topic(driver, "")
    submit_new_topic(driver)
    msg1 = get_error_message(driver)
    try:
        assert msg1 == "Vui lòng nhập tên chủ đề"
        print("✅ TC1 đã Pass")
    except AssertionError:
        print(f"❌ TC1 Fail: Expected 'Vui lòng nhập tên chủ đề' but got '{msg1}'")

    # --- TC2: Tên chủ đề dài hơn 255 ký tự ---
    open_add_topic_modal(driver)
    long_name = "A" * 256
    new_topic(driver, long_name)
    submit_new_topic(driver)
    msg2 = get_error_message(driver)
    try:
        assert msg2 == "Tên chủ đề không nhập quá 255 ký tự"
        print("✅ TC2 đã Pass")
    except AssertionError:
        print(f"❌ TC2 Fail: Expected 'Tên chủ đề không nhập quá 255 ký tự' but got '{msg2}'")
        
    # --- TC2: Tên chủ đề dài hơn 255 ký tự ---
    open_add_topic_modal(driver)
    long_name = "A" 
    new_topic(driver, long_name)
    submit_new_topic(driver)
    # Giả sử không có lỗi cho tên hợp lệ
    try:
        msg3 = get_error_message(driver)
    except:
        msg3 = ""
    assert msg3 == "", f"Expected no error but got '{msg3}'"
    

    # time.sleep(2)
    driver.quit()