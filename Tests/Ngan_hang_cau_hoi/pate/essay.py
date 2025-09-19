import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException


def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    print("✅ Mở modal tạo câu hỏi mới")
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    print("✅ Click chọn chủ đề")

def select_parent_option(driver, parent_title):
    wait = WebDriverWait(driver, 20)
    parent_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[title='{parent_title}']")))
    driver.execute_script("arguments[0].click();", parent_btn)
    time.sleep(1)
    print(f"✅ Chọn chủ đề cha: {parent_title}")

def chon_muc_do(driver, level: int):
    wait = WebDriverWait(driver, 20)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]")))
    driver.execute_script("arguments[0].click();", button)
    print(f"✅ Chọn mức độ {level}")

def choose_question_type(driver, option_text):
    wait = WebDriverWait(driver, 20)
    
    # 1️⃣ Lấy thẻ <select> trong modal
    select_elem = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "div[data-modal='data-modal'] div form div div select")
    ))
    
    # 2️⃣ Dùng Select của Selenium để chọn option theo text
    select = Select(select_elem)
    select.select_by_visible_text(option_text)
    
    # 3️⃣ Optional: verify giá trị đã chọn
    selected = select.first_selected_option.text
    print(f"✅ Đã chọn dạng câu hỏi: {selected}")


def cau_hoi(driver, question: str):
    wait = WebDriverWait(driver, 20)
    q_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", q_input)
    q_input.clear()
    q_input.send_keys(question)
    print(f"✅ Nhập câu hỏi: {question}")

def upload_file(driver, file_path: str):
    wait = WebDriverWait(driver, 20)
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input.send_keys(file_path)
    print(f"✅ Upload file: {file_path}")


def nhap_tags(driver, tags_text: str):
    wait = WebDriverWait(driver, 20)
    tag_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nhập thẻ (Ngăn cách bằng các dấu phẩy)']")))
    tag_input.clear()
    tag_input.send_keys(tags_text)
    print(f"✅ Nhập thẻ: {tags_text}")

def nhap_ghi_chu(driver, note_text: str):
    wait = WebDriverWait(driver, 20)
    note_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Nhập ghi chú']")))
    note_input.clear()
    note_input.send_keys(note_text)
    print(f"✅ Nhập ghi chú: {note_text}")

def remove_focus(driver):
    """
    Bỏ focus khỏi input/textarea trước khi submit.
    """
    driver.execute_script("document.activeElement.blur();")
    print("✅ Đã bỏ focus khỏi input")


def click_them_moi(driver):
    wait = WebDriverWait(driver, 20)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
    driver.execute_script("arguments[0].click();", btn)
    print("✅ Click Thêm mới (submit)")

@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    go_to_question_bank(driver)
    open_add_topic_modal(driver)
    select_parent_option(driver, "All in")
    choose_question_type(driver, "Tự luận")
    chon_muc_do(driver, 2)
    
    upload_file(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg")
    cau_hoi(driver, "Câu hỏi tự động tự luận 18/09")
    
    nhap_ghi_chu(driver, "Đây là ghi chú tự động")
    nhap_tags(driver, "Toán,Lý,Hóa")
    
    # trước khi click Thêm mới
    remove_focus(driver)
    click_them_moi(driver)
    time.sleep(5)
    driver.quit()
