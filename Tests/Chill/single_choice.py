import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

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
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    print("✅ Mở modal tạo câu hỏi mới")

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
    
# def chuyen_sang_dap_an_image_js(driver):
#     """
#     Click nút để chuyển sang chế độ nhập đáp án dạng ảnh bằng JavaScript.
#     """
#     wait = WebDriverWait(driver, 20)

#     image_btn = wait.until(EC.presence_of_element_located((
#         By.XPATH, "//div[contains(@class,'col-span-2 flex flex-col gap-1.5')]//button[2]"
#     )))

#     driver.execute_script("""
#         var btn = arguments[0];
#         var evt = new MouseEvent('click', {view: window, bubbles: true, cancelable: true});
#         btn.dispatchEvent(evt);
#     """, image_btn)

#     print("✅ Chuyển sang kiểu đáp án: image (JS click)")

def nhap_dap_an_flex(driver, answers: list[str]):
    wait = WebDriverWait(driver, 20)
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

# def click_radio_button(driver):
#     try:
#         wait = WebDriverWait(driver, 10)
#         # chọn svg thứ 142
#         radio_btn = wait.until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "(//*[name()='svg'][contains(@class,'tabler-icon tabler-icon-circle flex-none text-neutral-800 dark:text-neutral-200')])[3]")
#             )
#         )
#         radio_btn.click()
#         print("✅ Đã click vào radio button.")
#     except Exception as e:
#         print(f"❌ Lỗi khi click radio button: {e}")

def click_radio_button(driver, level: int):
    wait = WebDriverWait(driver, 20)
    position = level + 1 
    radio_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//*[name()='svg'][contains(@class,'tabler-icon tabler-icon-circle flex-none text-neutral-800 dark:text-neutral-200')])[{position}]")))
    radio_btn.click()
    print(f"✅ Chọn đáp án {position}")

# def select_answer(driver, index, container_css="div[data-modal='data-modal']", timeout=10):
#     """
#     Chọn đáp án theo thứ tự index (1..10).
#     - Tìm các svg chỉ trong container (mặc định div[data-modal='data-modal']).
#     - Click vào ancestor::button của svg (an toàn hơn).
#     - Scroll vào view, fallback dùng JS click khi cần.
#     """
#     if index < 1:
#         raise ValueError("index phải >= 1")
#     try:
#         wait = WebDriverWait(driver, timeout)

#         # 1) tìm container (nếu không tìm được thì dùng toàn document)
#         try:
#             container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, container_css)))
#         except TimeoutException:
#             container = driver  # fallback: tìm trong toàn document

#         # 2) lấy danh sách svg ứng viên (chỉ trong container)
#         svgs = container.find_elements(By.XPATH, ".//*[name()='svg' and contains(@class,'tabler-icon tabler-icon-circle')]")
#         print(f"[debug] Tìm thấy {len(svgs)} svg ứng viên trong container")

#         if not svgs:
#             raise Exception("Không tìm thấy svg nào match selector trong container. Kiểm tra container_css hoặc selector.")

#         # 3) nếu index lớn hơn số svg tìm thấy -> báo lỗi kèm debug
#         if index > len(svgs):
#             # in 1 vài svg đầu để debug
#             for i, s in enumerate(svgs[:10], start=1):
#                 print(f"  {i}: class={s.get_attribute('class')}, outerHTML[:120]={s.get_attribute('outerHTML')[:120]!r}")
#             raise IndexError(f"Index {index} > số svg tìm thấy ({len(svgs)}). Có thể cần đổi container_css hoặc offset.")

#         # 4) target svg trong container: (index-1)
#         target_svg = svgs[index - 1]

#         # 5) tìm button cha (nếu không có thì click svg)
#         try:
#             target_button = target_svg.find_element(By.XPATH, "./ancestor::button[1]")
#         except Exception:
#             target_button = target_svg

#         # 6) scroll vào giữa màn hình
#         driver.execute_script("arguments[0].scrollIntoView({block:'center'})", target_button)

#         # 7) đợi element hiển thị & enabled rồi click, fallback JS khi intercept
#         wait.until(lambda d: target_button.is_displayed() and target_button.is_enabled())
#         try:
#             target_button.click()
#         except ElementClickInterceptedException:
#             driver.execute_script("arguments[0].click();", target_button)

#         print(f"✅ Đã click đáp án {index} (dựa trên danh sách svg trong container).")

#     except Exception as e:
#         print(f"❌ Lỗi khi chọn đáp án {index}: {e}")
#         raise



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
    # chon_muc_do(driver, 2)

    cau_hoi(driver, "Câu hỏi tự động 12345")
    nhap_dap_an_flex(driver, ["Đáp án A","Đáp án B","Đáp án C","Đáp án D","Đáp án E","Đáp án F"])
    # nhap_tags(driver, "Toán,Lý,Hóa")
    # nhap_ghi_chu(driver, "Đây là ghi chú tự động")
    # upload_file(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg")
    click_radio_button(driver, 3)
    # select_answer(driver, 2)
    # trước khi click Thêm mới
    remove_focus(driver)
    # click_them_moi(driver)
    time.sleep(5)
    driver.quit()
