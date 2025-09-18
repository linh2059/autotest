import pytest
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from Pages.utils import get_wait


# ======== HÀM ĐỌC EXCEL LẦN LƯỢT ========
def read_excel_row_by_row(file_path):
    df = pd.read_excel(file_path)
    df['answers'] = df['answers'].apply(lambda x: [a.strip() for a in x.split(',')])
    df['diem'] = df['diem'].apply(lambda x: [int(a.strip()) for a in x.split(',')])
    for _, row in df.iterrows():
        yield row.to_dict()


# ======== HÀM HELPER ========
def wait_for_clickable(driver, by, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, locator)))

def go_to_question_bank(driver):
    wait = get_wait(driver)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = get_wait(driver)
    driver.execute_script("arguments[0].click();", wait_for_clickable(driver, By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))
    driver.execute_script("arguments[0].click();", wait_for_clickable(driver, By.XPATH, "//p[@class='text-sm']"))
    # Đợi modal load xong
    wait_for_clickable(driver, By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']", 20)
    print("✅ Mở modal tạo câu hỏi mới")

def select_parent_option(driver, parent_title):
    parent_btn = wait_for_clickable(driver, By.CSS_SELECTOR, f"button[title='{parent_title}']")
    driver.execute_script("arguments[0].click();", parent_btn)
    time.sleep(0.5)
    print(f"✅ Chọn chủ đề cha: {parent_title}")

def chon_muc_do(driver, level: int):
    button = wait_for_clickable(driver, By.XPATH, f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]")
    driver.execute_script("arguments[0].click();", button)
    print(f"✅ Chọn mức độ {level}")

def choose_question_type(driver, option_text):
    select_elem = wait_for_clickable(driver, By.CSS_SELECTOR, "div[data-modal='data-modal'] div form div div select")
    select = Select(select_elem)
    select.select_by_visible_text(option_text)
    print(f"✅ Đã chọn dạng câu hỏi: {select.first_selected_option.text}")

def cau_hoi(driver, question: str):
    q_input = wait_for_clickable(driver, By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']")
    driver.execute_script("arguments[0].scrollIntoView(true);", q_input)
    q_input.clear()
    q_input.send_keys(question)
    print(f"✅ Nhập câu hỏi: {question}")

def upload_file(driver, file_path: str):
    file_input = wait_for_clickable(driver, By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(file_path)
    print(f"✅ Upload file: {file_path}")

def nhap_dap_an_flex(driver, answers: list[str]):
    for i, ans in enumerate(answers, start=1):
        if i > 4:
            add_btn = wait_for_clickable(driver, By.XPATH, "//button[contains(text(),'Thêm câu trả lời')]")
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(0.3)
            print(f"✅ Click thêm đáp án thứ {i}")
        input_xpath = f"(//input[contains(@placeholder,'Nhập câu trả lời')])[{i}]"
        ans_input = wait_for_clickable(driver, By.XPATH, input_xpath)
        ans_input.clear()
        ans_input.send_keys(ans)
        print(f"✅ Nhập đáp án {i}: {ans}")
        if i == 10:
            print("⚠️ Đạt tối đa 10 đáp án")
            break

def chon_diem_cho_dap_an(driver, answer_index: int, diem: int):
    select_xpath = f"(//div[@data-modal='data-modal']//select)[{answer_index}]"
    select_elem = wait_for_clickable(driver, By.XPATH, select_xpath)
    driver.execute_script("arguments[0].scrollIntoView(true);", select_elem)
    time.sleep(0.2)
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'))", select_elem, str(diem))
    print(f"✅ Chọn điểm {diem} cho đáp án {answer_index}")

def nhap_tags(driver, tags_text: str):
    tag_input = wait_for_clickable(driver, By.XPATH, "//input[@placeholder='Nhập thẻ (Ngăn cách bằng các dấu phẩy)']")
    tag_input.clear()
    tag_input.send_keys(tags_text)
    print(f"✅ Nhập thẻ: {tags_text}")

def nhap_ghi_chu(driver, note_text: str):
    note_input = wait_for_clickable(driver, By.XPATH, "//textarea[@placeholder='Nhập ghi chú']")
    note_input.clear()
    note_input.send_keys(note_text)
    print(f"✅ Nhập ghi chú: {note_text}")

def remove_focus(driver):
    driver.execute_script("document.activeElement.blur();")
    print("✅ Đã bỏ focus khỏi input")

def click_them_moi(driver):
    btn = wait_for_clickable(driver, By.XPATH, "//button[contains(text(),'Thêm mới')]")
    driver.execute_script("arguments[0].click();", btn)
    print("✅ Click Thêm mới (submit)")


# ======== TEST CASE ========
@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_excel(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    for i, data in enumerate(read_excel_row_by_row(r"C:\Users\admin\Documents\Selenium\File\fill_in_the_blank.xlsx"), start=1):
        try:
            go_to_question_bank(driver)
            open_add_topic_modal(driver)
            upload_file(driver, data['file_path'])
            select_parent_option(driver, data['parent_title'])

            choose_question_type(driver, data['question_type'])
            chon_muc_do(driver, data['level'])

            cau_hoi(driver, data['question'])
            nhap_dap_an_flex(driver, data['answers'])

            for idx, diem in enumerate(data['diem'], start=1):
                chon_diem_cho_dap_an(driver, idx, diem)

            nhap_tags(driver, data['tags'])
            nhap_ghi_chu(driver, data['note'])

            remove_focus(driver)
            click_them_moi(driver)
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Lỗi ở dòng {i}: {e}")
