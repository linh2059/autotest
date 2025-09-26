import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    # demo_pause() 
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    print("✅ Mở modal tạo câu hỏi mới")

def click_them_moi(driver):
    wait = WebDriverWait(driver, 20)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
    driver.execute_script("arguments[0].click();", btn)
    # demo_pause() 
    print("✅ Click Thêm mới (submit)")


def cau_hoi(driver, question: str):
    wait = WebDriverWait(driver, 20)
    q_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", q_input)
    q_input.clear()
    q_input.send_keys(question)
    print(f"✅ Nhập câu hỏi: {question if question else '[Trống]'}")


def check_message(driver, expected_error: str):
    wait = WebDriverWait(driver, 20)
    error_label = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//textarea[@placeholder='Nhập câu hỏi']"
            "/following-sibling::label[contains(@class,'error-element-custom')]"
        ))
    )
    actual_text = error_label.text.strip()
    print(f"⚠️ Message hiển thị: '{actual_text}'")
    assert actual_text == expected_error, (
        f"❌ Sai message!\n"
        f"Expected: '{expected_error}'\n"
        f"Actual:   '{actual_text}'"
    )
    print("✅ Message đúng như mong muốn")


def remove_focus(driver):
    """
    Bỏ focus khỏi input/textarea trước khi submit.
    """
    driver.execute_script("document.activeElement.blur();")
    print("✅ Đã bỏ focus khỏi input")


@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    go_to_question_bank(driver)
    open_add_topic_modal(driver)
    
    # cau_hoi(driver, "")
    # click_them_moi(driver)
    # check_message(driver, "Vui lòng nhập câu hỏi")

    # TH2: quá 10000 ký tự
    cau_hoi(driver, "a" * 100001)
    remove_focus(driver)
    time.sleep(10)
    click_them_moi(driver)
    check_message(driver, "Câu hỏi không nhập quá 10000 ký tự")
    # cau_hoi(driver, "", expected_error="Vui lòng nhập câu hỏi")
    time.sleep(10)
    driver.quit()
    # document.querySelectorAll("input[type=file]")
