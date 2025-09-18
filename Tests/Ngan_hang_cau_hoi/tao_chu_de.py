import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.login_page import LoginPage


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


def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)

    # --- Click nút 'Thêm chủ đề' ---
    add_topic_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm chủ đề')]"))
    )
    driver.execute_script("arguments[0].click();", add_topic_btn)
    print("✅ Đã click nút Thêm chủ đề")

    # --- Chờ modal hiển thị input ---
    modal_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'modal')]//input[@placeholder='Nhập tên chủ đề']"))
    )
    print("✅ Modal Thêm chủ đề hiển thị")

    return modal_input


def submit_new_topic(driver, ten_chu_de="Chủ đề auto"):
    wait = WebDriverWait(driver, 20)

    # --- Lấy lại input trong modal ---
    modal_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//input[@placeholder='Nhập tên chủ đề']"))
    )

    # --- Chỉ dùng Cách 2: Inject JS + trigger event ---
    driver.execute_script("""
        let input = arguments[0];
        let lastValue = input.value;
        input.value = arguments[1];
        let event = new Event('input', { bubbles: true });
        event.simulated = true;
        let tracker = input._valueTracker;
        if (tracker) {
            tracker.setValue(lastValue);
        }
        input.dispatchEvent(event);
    """, modal_input, ten_chu_de)
    
    # --- Click 'Thêm mới' ---
    save_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]"))
    )
    driver.execute_script("arguments[0].click();", save_btn)
    print("💾 Đã click Thêm mới để tạo chủ đề")



@pytest.mark.usefixtures("driver")
def test_tao_chu_de(driver):
    # --- Login ---
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    # --- Vào Ngân hàng câu hỏi ---
    go_to_question_bank(driver)

    # --- Mở modal Thêm chủ đề ---
    open_add_topic_modal(driver)

    # --- Nhập và submit ---
    submit_new_topic(driver, "Chủ đề auto")

    time.sleep(2)
    driver.quit()
