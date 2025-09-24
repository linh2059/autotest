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
    print("✅ Mở modal tạo câu hỏi mới")

def open_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    print("✅ Click chọn chủ đề")

def select_topic(driver, path, timeout=15):
    """
    Truyền path dạng: 'All in -> Có file đính kèm -> file doc'
    """
    wait = WebDriverWait(driver, timeout)
    topics = [t.strip() for t in path.split("->")]

    for parent in topics[:-1]:
        try:
            # Tìm chính nút chứa text parent
            parent_btn = wait.until(
                EC.presence_of_element_located((By.XPATH, f"//button[@title='{parent}']"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", parent_btn)

            # TH1: Có icon riêng (sibling)
            try:
                dropdown_btn = parent_btn.find_element(By.XPATH, "./preceding-sibling::button[1]")
            except:
                # TH2: Icon nằm chung trong cùng button
                try:
                    dropdown_btn = parent_btn.find_element(By.XPATH, ".//*[name()='svg']")
                except:
                    dropdown_btn = parent_btn  # fallback: click thẳng vào chính button

            # Mở dropdown nếu chưa mở
            aria_expanded = dropdown_btn.get_attribute("aria-expanded")
            if not aria_expanded or aria_expanded == "false":
                driver.execute_script("arguments[0].click();", dropdown_btn)
                print(f"✅ Đã mở dropdown của: {parent}")
        except Exception as e:
            raise Exception(f"❌ Không tìm thấy hoặc không click được dropdown '{parent}'") from e

    # Click chủ đề cuối
    final_topic = topics[-1]
    final_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//button[@title='{final_topic}']"))
    )
    driver.execute_script("arguments[0].click();", final_btn)
    print(f"🎯 Đã chọn chủ đề: {final_topic}")

def chuyen_sang_dap_an_image_js(driver):
    """
    Click nút để chuyển sang chế độ nhập đáp án dạng ảnh bằng JavaScript.
    """
    wait = WebDriverWait(driver, 20)

    image_btn = wait.until(EC.presence_of_element_located((
        By.XPATH, "//div[contains(@class,'col-span-2 flex flex-col gap-1.5')]//button[2]"
    )))

    driver.execute_script("""
        var btn = arguments[0];
        var evt = new MouseEvent('click', {view: window, bubbles: true, cancelable: true});
        btn.dispatchEvent(evt);
    """, image_btn)

    print("✅ Chuyển sang kiểu đáp án: image (JS click)")

def upload_file(driver, file_path: str):
    wait = WebDriverWait(driver, 20)
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input.send_keys(file_path)
    print(f"✅ Upload file: {file_path}")

def upload_images(driver, answers):
    wait = WebDriverWait(driver, 10)

    for i, file_path in enumerate(answers, start=1):
        # Nếu số đáp án > 4 thì bấm nút thêm
        if i > 4:
            add_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm câu trả lời')]"))
            )
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(0.5)
            print(f"✅ Click thêm đáp án thứ {i}")

        # Thực tế input index = i + 1
        input_xpath = f"(//input[@type='file'])[ {i+1} ]"
        input_elem = wait.until(EC.presence_of_element_located((By.XPATH, input_xpath)))

        driver.execute_script("arguments[0].style.display='block';", input_elem)
        input_elem.send_keys(file_path)

        print(f"✅ Upload file '{file_path}' vào đáp án {i}")

def click_radio_button(driver, level: int):
    wait = WebDriverWait(driver, 20)
    position = level + 4
    radio_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//*[name()='svg'][contains(@class,'tabler-icon tabler-icon-circle flex-none text-neutral-800 dark:text-neutral-200')])[{position}]")))
    radio_btn.click()
    print(f"✅ Chọn đáp án {position} làm đáp án đúng")

@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    go_to_question_bank(driver)
    open_add_topic_modal(driver)
    open_topic_modal(driver)
    # click_parent_dropdown(driver, "All in")
    # click_parent_dropdown(driver, "Có file đính kèm")
    
    # select_parent_option(driver, "file doc")

    # Case 1: Chủ đề có nhiều cấp
    select_topic(driver, "All in -> Có file đính kèm -> file doc")
    chuyen_sang_dap_an_image_js(driver)
    # Case 2: Chủ đề chỉ 1 cấp
    # select_topic(driver, "Chủ đề auto")
    upload_file(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg")

    # upload_image(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg", answer_index=1)  # Upload cho đáp án 1
    # upload_image(driver, r"C:\Users\admin\Pictures\Screenshot_1.png", answer_index=2) # Upload cho đáp án 2
    # upload_image(driver, r"C:\Users\admin\Pictures\Screenshot_2.png", answer_index=3) # Upload cho đáp án 2
    # upload_image(driver, r"C:\Users\admin\Pictures\Screenshot_1.png", answer_index=4) # Upload cho đáp án 2
    # upload_image(driver, r"C:\Users\admin\Pictures\Screenshot_1.png", answer_index=5) # Upload cho đáp án 2

    # answers = [
    # r"C:\Users\admin\Pictures\Screenshot_1.png",
    # r"C:\Users\admin\Pictures\Screenshot_2.png",
    # r"C:\Users\admin\Pictures\Screenshot_1.png",
    # r"C:\Users\admin\Pictures\Screenshot_2.png",
    # r"C:\Users\admin\Pictures\Screenshot_1.png",
    # ]
    # upload_images(driver, answers)

    click_radio_button(driver, 4)


    time.sleep(5)
    driver.quit()
    # document.querySelectorAll("input[type=file]")
