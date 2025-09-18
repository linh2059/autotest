import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from Pages.utils import get_wait
import pandas as pd

def read_excel_row_by_row(file_path):
    df = pd.read_excel(file_path)
    df['answers'] = df['answers'].apply(lambda x: [a.strip() for a in x.split(',')])
    df['diem'] = df['diem'].apply(lambda x: [int(a.strip()) for a in x.split(',')])
    for _, row in df.iterrows():
        yield row.to_dict()




def go_to_question_bank(driver):
    wait = get_wait(driver)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = get_wait(driver)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    print("✅ Mở modal tạo câu hỏi mới")

def select_parent_option(driver, parent_title):
    wait = get_wait(driver)
    parent_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[title='{parent_title}']")))
    driver.execute_script("arguments[0].click();", parent_btn)
    time.sleep(1)
    print(f"✅ Chọn chủ đề cha: {parent_title}")

def chon_muc_do(driver, level: int):
    wait = get_wait(driver)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]")))
    driver.execute_script("arguments[0].click();", button)
    print(f"✅ Chọn mức độ {level}")

def choose_question_type(driver, option_text):
    wait = get_wait(driver)
    
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
    wait = get_wait(driver)
    q_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", q_input)
    q_input.clear()
    q_input.send_keys(question)
    print(f"✅ Nhập câu hỏi: {question}")

def upload_file(driver, file_path: str):
    wait = get_wait(driver)
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input.send_keys(file_path)
    print(f"✅ Upload file: {file_path}")

def nhap_dap_an_flex(driver, answers: list[str]):
    wait = get_wait(driver)
    for i, ans in enumerate(answers, start=1):
        if i > 4:
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm câu trả lời')]")))
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(0.5)
            print(f"✅ Click thêm đáp án thứ {i}")
        input_xpath = f"(//input[contains(@placeholder,'Nhập câu trả lời')])[{i}]"
        ans_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        ans_input.clear()
        ans_input.send_keys(ans)
        print(f"✅ Nhập đáp án {i}: {ans}")
        if i == 10:
            print("⚠️ Đạt tối đa 10 đáp án")
            break

from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import Select

def chon_diem_cho_dap_an(driver, answer_index: int, diem: int):
    """
    answer_index: số thứ tự đáp án (1,2,3...)
    diem: điểm muốn chọn (0,1,2,3)
    """
    wait = WebDriverWait(driver, 10)

    # Lấy select theo thứ tự đáp án
    select_xpath = f"(//div[@data-modal='data-modal']//select)[{answer_index}]"
    select_elem = wait.until(EC.presence_of_element_located((By.XPATH, select_xpath)))

    # Scroll vào view
    driver.execute_script("arguments[0].scrollIntoView(true);", select_elem)
    time.sleep(0.2)  # đợi render

    # Chọn value bằng JS
    driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'))", select_elem, str(diem))
    print(f"✅ Chọn điểm {diem} cho đáp án {answer_index}")




def nhap_tags(driver, tags_text: str):
    wait = get_wait(driver)
    tag_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nhập thẻ (Ngăn cách bằng các dấu phẩy)']")))
    tag_input.clear()
    tag_input.send_keys(tags_text)
    print(f"✅ Nhập thẻ: {tags_text}")

def nhap_ghi_chu(driver, note_text: str):
    wait = get_wait(driver)
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
    wait = get_wait(driver)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
    driver.execute_script("arguments[0].click();", btn)
    print("✅ Click Thêm mới (submit)")

@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_excel(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    for data in read_excel_row_by_row(r"C:\Users\admin\Documents\Selenium\File\fill_in_the_blank.xlsx"):
        go_to_question_bank(driver)
        open_add_topic_modal(driver)
        upload_file(driver, data['file_path'])
        select_parent_option(driver, data['parent_title'])

        choose_question_type(driver, data['question_type'])
        chon_muc_do(driver, data['level'])

        cau_hoi(driver, data['question'])
        nhap_dap_an_flex(driver, data['answers'])

        # Chọn điểm cho từng đáp án
        for i, diem in enumerate(data['diem'], start=1):
            chon_diem_cho_dap_an(driver, i, diem)

        nhap_tags(driver, data['tags'])
        nhap_ghi_chu(driver, data['note'])

        remove_focus(driver)
        click_them_moi(driver)
        time.sleep(5)
