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
    wait = WebDriverWait(driver, 50)

    # --- Click nút 'Thêm chủ đề' ---
    add_topic_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))
    )
    driver.execute_script("arguments[0].click();", add_topic_btn)
    print("✅ Đã click nút Tạo câu hỏi mới")

    topic_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))
    )
    driver.execute_script("arguments[0].click();", topic_btn)
    print("✅ Đã click vào chọn chủ đề")

def select_parent_option(driver, parent_title):
    wait = WebDriverWait(driver, 20)

    # --- Tìm nút cha ---
    parent_btn = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, f"button[title='{parent_title}']"
    )))

    # --- Click bằng JS ---
    driver.execute_script("arguments[0].click();", parent_btn)
    print(f"✅ Đã click cha: {parent_title}")

    # --- Đợi danh sách con (nếu có) hiện ra ---
    time.sleep(1)  # hoặc dùng wait với child nếu biết trước


# def select_child_option(driver, parent_title):
#     wait = WebDriverWait(driver, 50)

#     # --- 1. Xác định cha ---
#     parent = wait.until(EC.presence_of_element_located((
#         By.CSS_SELECTOR, f"button[title='{parent_title}']"
#     )))
#     parent.click()
#     print(f"✅ Đã chọn {parent_title}")

def chon_muc_do(driver, level: int):
    wait = WebDriverWait(driver, 50)
    xpath = f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]"
    button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].click();", button)
    print(f"✅ Đã chọn mức độ {level}")

    # --- 2. Kiểm tra con đã hiển thị chưa ---
    # child_xpath = f"//button[@title='{child_title}']"
    # try:
    #     child = driver.find_element(By.CSS_SELECTOR, child_xpath)
    #     if not child.is_displayed():
    #         parent.click()  # xổ ra
    #         wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, child_xpath)))
    # except:
    #     parent.click()  # xổ ra
    #     wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, child_xpath)))

    # # --- 3. Click chọn con ---
    # child = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, child_xpath)))
    # child.click()
    # print(f"✅ Đã chọn {child_title}")

def cau_hoi(driver, question):
    wait = WebDriverWait(driver, 40)

    question_input = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", question_input)
    question_input.clear()
    question_input.send_keys(question)
    print(f"✅ Đã nhập câu hỏi: {question}")


def upload_file(driver, file_path: str):
    wait = WebDriverWait(driver, 20)

    # Tìm input[type=file] trong modal
    file_input = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, "input[type='file']"
    )))

    # Gửi absolute path đến file
    file_input.send_keys(file_path)
    print(f"✅ Đã upload file: {file_path}")

# def nhap_dap_an(driver, answers: list[str]):
#     """
#     Nhập đáp án vào các input sẵn có trong modal tạo câu hỏi.
#     answers: list các đáp án, ví dụ ["Đáp án 1", "Đáp án 2", ...]
#     """
#     wait = WebDriverWait(driver, 20)
    
#     for i, ans in enumerate(answers, start=1):
#         input_xpath = f"(//input[contains(@placeholder,'Nhập câu trả lời')])[{i}]"
#         ans_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
#         ans_input.clear()
#         ans_input.send_keys(ans)
#         print(f"✅ Đã nhập đáp án {i}: {ans}")
#         time.sleep(0.5)  # optional: chờ nhẹ

def nhap_dap_an_flex(driver, answers: list[str]):
    """
    Nhập đáp án vào modal tạo câu hỏi, tự động click 'Thêm câu trả lời' nếu >4 đáp án.
    answers: list các đáp án, ví dụ ["Đáp án 1", "Đáp án 2", ...]
    """
    wait = WebDriverWait(driver, 20)
    
    for i, ans in enumerate(answers, start=1):
        # --- Nếu i > số input mặc định (4), click 'Thêm câu trả lời'
        if i > 4:
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm câu trả lời')]")))
            driver.execute_script("arguments[0].click();", add_btn)
            print(f"✅ Click thêm đáp án thứ {i}")
            time.sleep(0.5)  # chờ input mới render
        
        # --- Chọn input thứ i
        input_xpath = f"(//input[contains(@placeholder,'Nhập câu trả lời')])[{i}]"
        ans_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        ans_input.clear()
        ans_input.send_keys(ans)
        print(f"✅ Nhập đáp án {i}: {ans}")
        time.sleep(0.3)
        
        # --- Giới hạn tối đa 10 đáp án ---
        if i == 10:
            print("⚠️ Đã đạt tối đa 10 đáp án, dừng thêm.")
            break

def nhap_tags(driver, tags_text: str):
    """
    Nhập đoạn text vào input 'Nhập thẻ (Ngăn cách bằng các dấu phẩy)'
    tags_text: ví dụ "Toán,Lý,Hóa"
    """
    wait = WebDriverWait(driver, 20)
    
    tag_input = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//input[@placeholder='Nhập thẻ (Ngăn cách bằng các dấu phẩy)']"
    )))
    
    tag_input.clear()
    tag_input.send_keys(tags_text)
    print(f"✅ Đã nhập thẻ: {tags_text}")

def nhap_ghi_chu(driver, note_text: str):
    """
    Nhập text vào ô Ghi chú
    note_text: nội dung ghi chú
    """
    wait = WebDriverWait(driver, 20)
    
    note_input = wait.until(EC.visibility_of_element_located((
        By.XPATH, "//textarea[@placeholder='Nhập ghi chú']"
    )))
    
    note_input.clear()
    note_input.send_keys(note_text)
    print(f"✅ Đã nhập ghi chú: {note_text}")

# def click_them_moi(driver):
#     """
#     Click vào nút 'Thêm mới' trong modal tạo câu hỏi
#     """
#     wait = WebDriverWait(driver, 20)

#     # --- Tìm button 'Thêm mới' ---
#     them_moi_btn = wait.until(EC.element_to_be_clickable((
#         By.XPATH, "//button[contains(text(),'Thêm mới')]"
#     )))

#     # --- Click bằng JS (tránh bị block) ---
#     driver.execute_script("arguments[0].click();", them_moi_btn)
#     print("✅ Đã click nút Thêm mới")


@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi(driver):
    # --- Login ---
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    # --- Vào Ngân hàng câu hỏi ---
    go_to_question_bank(driver)

    # --- Mở modal Thêm chủ đề ---
    open_add_topic_modal(driver)

    # Chọn chủ đề cha
    select_parent_option(driver, "All in")

    # chon_muc_do(driver, 1)  # chọn mức 1
    chon_muc_do(driver, 2)  # chọn mức 2
    # chon_muc_do(driver, 3)  # chọn mức 3

    
    upload_file(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg")
    

    cau_hoi(driver, "Câu hỏi tự động 12345")
# nhap_dap_an(driver, ["Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D"])
    
    nhap_dap_an_flex(driver, [
    "Đáp án A", "Đáp án B", "Đáp án C", "Đáp án D", 
    "Đáp án E", "Đáp án F"
])

    nhap_tags(driver, "Toán,Lý,Hóa")

    nhap_ghi_chu(driver, "Đây là ghi chú tự động")
    
    # click_them_moi(driver)
    

    # --- Nhập và submit ---
    submit_new_topic(driver, "Chủ đề auto")
    time.sleep(20)
    driver.quit()

