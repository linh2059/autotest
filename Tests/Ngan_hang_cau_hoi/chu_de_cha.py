import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Pages.login_page import LoginPage


def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu_locator = (By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")
    menu = wait.until(EC.element_to_be_clickable(menu_locator))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    print("✅ Đã click menu Ngân hàng câu hỏi")

    try:
        wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    except TimeoutException:
        raise Exception(f"❌ Không chuyển sang trang Ngân hàng câu hỏi, URL hiện tại: {driver.current_url}")
    print(f"🎉 Đã vào trang: {driver.current_url}")


def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    add_topic_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm chủ đề')]"))
    )
    driver.execute_script("arguments[0].click();", add_topic_btn)
    print("✅ Đã click nút Thêm chủ đề")

    modal_input = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'modal')]//input[@placeholder='Nhập tên chủ đề']"))
    )
    print("✅ Modal Thêm chủ đề hiển thị")
    return modal_input


# def input_topic_name(driver, ten_chu_de):
#     """
#     Nhập tên chủ đề vào modal (tách riêng).
#     """
#     wait = WebDriverWait(driver, 20)
#     modal_input = wait.until(
#         EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//input[@placeholder='Nhập tên chủ đề']"))
#     )

#     driver.execute_script("""
#         let input = arguments[0];
#         let lastValue = input.value;
#         input.value = arguments[1];
#         let event = new Event('input', { bubbles: true });
#         event.simulated = true;
#         let tracker = input._valueTracker;
#         if (tracker) {
#             tracker.setValue(lastValue);
#         }
#         input.dispatchEvent(event);
#     """, modal_input, ten_chu_de)
#     print(f"✅ Nhập tên chủ đề: {ten_chu_de}")

def remove_focus(driver):
    """
    Bỏ focus khỏi input/textarea trước khi submit.
    """
    driver.execute_script("document.activeElement.blur();")
    print("✅ Đã bỏ focus khỏi input")

# def click_them_moi(driver):
#     wait = WebDriverWait(driver, 20)
#     btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
#     driver.execute_script("arguments[0].click();", btn)
#     print("✅ Click Thêm mới (submit)")

# def click_them_moi(driver):
#     """
#     Click nút 'Thêm mới' trong modal (tách riêng).
#     """
#     wait = WebDriverWait(driver, 20)
#     save_btn = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]"))
#     )
#     driver.execute_script("arguments[0].click();", save_btn)
#     print("💾 Đã click Thêm mới để tạo chủ đề")


from selenium.webdriver.common.keys import Keys

def input_topic_name(driver, ten_chu_de):
    modal_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//input[@placeholder='Nhập tên chủ đề']"))
    )
    driver.execute_script("""
        let input = arguments[0];
        let lastValue = input.value;
        input.value = arguments[1];
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        let tracker = input._valueTracker;
        if (tracker) { tracker.setValue(lastValue); }
    """, modal_input, ten_chu_de)
    modal_input.send_keys(Keys.TAB)  # trigger blur
    print(f"✅ Nhập tên chủ đề: {ten_chu_de}")

def click_them_moi(driver):
    save_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]"))
    )
    WebDriverWait(driver, 5).until(lambda d: save_btn.is_enabled())
    driver.execute_script("arguments[0].click();", save_btn)
    print("💾 Đã click Thêm mới để tạo chủ đề")


@pytest.mark.usefixtures("driver")
def test_tao_chu_de(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    go_to_question_bank(driver)

    open_add_topic_modal(driver)

    input_topic_name(driver, "Chủ đề auto hehe")
    # trước khi click Thêm mới
    remove_focus(driver)
    click_them_moi(driver)

    time.sleep(5)
    driver.quit()
    
