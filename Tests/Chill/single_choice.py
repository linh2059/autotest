import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from selenium.common.exceptions import TimeoutException
from Pages.utils import get_wait, demo_pause


## Hàm vào trang Ngân hàng câu hỏi
def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    demo_pause() 
    print("✅ Vào trang Ngân hàng câu hỏi")

## Hàm mở modal tạo câu hỏi mới
def open_add_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    demo_pause() 
    print("✅ Mở modal tạo câu hỏi mới")

## Hàm mở modal chọn chủ đề
def open_topic_modal(driver):
    wait = WebDriverWait(driver, 20)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    demo_pause() 
    print("✅ Click chọn chủ đề")

## Hàm chọn chủ đề theo đường dẫn
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
    demo_pause() 
    print(f"🎯 Đã chọn chủ đề: {final_topic}")

## Hàm chuyển sang kiểu đáp án image 
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
    demo_pause() 

    print("✅ Chuyển sang kiểu đáp án: image (JS click)")

## Hàm upload file (ảnh, doc, pdf...)
def upload_file(driver, file_path: str):
    wait = WebDriverWait(driver, 20)
    file_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    file_input.send_keys(file_path)
    demo_pause() 
    print(f"✅ Upload file: {file_path}")

## Hàm upload ảnh cho từng đáp án
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
        demo_pause() 

        print(f"✅ Upload file '{file_path}' vào đáp án {i}")

## Hàm chọn mức độ
def chon_muc_do(driver, level: int):
    wait = WebDriverWait(driver, 20)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]")))
    driver.execute_script("arguments[0].click();", button)
    demo_pause() 
    print(f"✅ Chọn mức độ {level}")

## Hàm nhập câu hỏi
def cau_hoi(driver, question: str):
    wait = WebDriverWait(driver, 20)
    q_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea[placeholder='Nhập câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView(true);", q_input)
    q_input.clear()
    q_input.send_keys(question)
    demo_pause() 
    print(f"✅ Nhập câu hỏi: {question}")

## Hàm nhập đáp án dạng text
def nhap_dap_an_flex(driver, answers: list[str]):
    wait = WebDriverWait(driver, 20)
    for i, ans in enumerate(answers, start=1):
        if i > 4:
            add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm câu trả lời')]")))
            driver.execute_script("arguments[0].click();", add_btn)
            time.sleep(0.5)
            print(f"✅ Click thêm đáp án thứ {i}")
            demo_pause() 
        input_xpath = f"(//input[contains(@placeholder,'Nhập câu trả lời')])[{i}]"
        ans_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
        ans_input.clear()
        ans_input.send_keys(ans)
        demo_pause() 
        print(f"✅ Nhập đáp án {i}: {ans}")
        if i == 10:
            print("⚠️ Đạt tối đa 10 đáp án")
            break


## Hàm click nút radio để chọn đáp án đúng (dạng text)
def click_radio_button_text(driver, level: int):
    wait = WebDriverWait(driver, 20)
    position = level + 1 
    radio_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//*[name()='svg'][contains(@class,'tabler-icon tabler-icon-circle flex-none text-neutral-800 dark:text-neutral-200')])[{position}]")))
    radio_btn.click()
    demo_pause() 
    print(f"✅ Chọn đáp án {position}")

## Hàm click chọn đáp án đúng (radio button) cho image type
def click_radio_button_image(driver, level: int):
    wait = WebDriverWait(driver, 20)
    position = level + 4
    radio_btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//*[name()='svg'][contains(@class,'tabler-icon tabler-icon-circle flex-none text-neutral-800 dark:text-neutral-200')])[{position}]")))
    radio_btn.click()
    demo_pause() 
    print(f"✅ Chọn đáp án {position} làm đáp án đúng")

## Hàm nhập thẻ (tags)
def nhap_tags(driver, tags_text: str):
    wait = WebDriverWait(driver, 20)
    tag_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nhập thẻ (Ngăn cách bằng các dấu phẩy)']")))
    tag_input.clear()
    tag_input.send_keys(tags_text)
    demo_pause() 
    print(f"✅ Nhập thẻ: {tags_text}")

## Hàm nhập ghi chú
def nhap_ghi_chu(driver, note_text: str):
    wait = WebDriverWait(driver, 20)
    note_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Nhập ghi chú']")))
    note_input.clear()
    note_input.send_keys(note_text)
    demo_pause() 
    print(f"✅ Nhập ghi chú: {note_text}")

## Hàm bỏ focus khỏi input/textarea
def remove_focus(driver):
    """
    Bỏ focus khỏi input/textarea trước khi submit.
    """
    driver.execute_script("document.activeElement.blur();")
    print("✅ Đã bỏ focus khỏi input")

## Hàm click Thêm mới (submit)
def click_them_moi(driver):
    wait = WebDriverWait(driver, 20)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]")))
    driver.execute_script("arguments[0].click();", btn)
    demo_pause() 
    print("✅ Click Thêm mới (submit)")

@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    # Initialize and login
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    #Vào trang Ngân hàng câu hỏi
    go_to_question_bank(driver)

    ## Mở modal tạo câu hỏi mới
    open_add_topic_modal(driver)

    ## Mở modal chọn chủ đề
    open_topic_modal(driver)
    
    # chon_muc_do(driver, 2)

    # Case 1: Chủ đề có nhiều cấp
    select_topic(driver, "All in -> Có file đính kèm -> file doc")
    # Case 2: Chủ đề chỉ 1 cấp
    # select_topic(driver, "Chủ đề auto")

    
    # cau_hoi(driver, "Câu hỏi tự động 12345")
    # nhap_tags(driver, "Toán,Lý,Hóa")
    # nhap_ghi_chu(driver, "Đây là ghi chú tự động")

    ##Thêm tệp đính kèm chung cho câu hỏi
    upload_file(driver, r"C:\Users\admin\Pictures\3264fac23f6db6430fc869be212b45fb.jpg")


     # 🟢 Chọn type = "image" hoặc "text"
    answer_type = "image"   # đổi thành "text" nếu muốn

    try:
        if answer_type == "image":
            chuyen_sang_dap_an_image_js(driver)

            answers = [
                r"C:\Users\admin\Pictures\Screenshot_1.png",
                r"C:\Users\admin\Pictures\Screenshot_2.png",
                r"C:\Users\admin\Pictures\Screenshot_1.png",
                r"C:\Users\admin\Pictures\Screenshot_2.png",
                r"C:\Users\admin\Pictures\Screenshot_1.png",
            ]
            upload_images(driver, answers)
            click_radio_button_image(driver, 3)

        elif answer_type == "text":
            nhap_dap_an_flex(driver, [
                "Đáp án A", "Đáp án B", "Đáp án C",
                "Đáp án D", "Đáp án E", "Đáp án F"
            ])
            click_radio_button_text(driver, 3)

    except TimeoutException:
        print(f"⚠️ {answer_type} mode không khả dụng")

    cau_hoi(driver, "Câu hỏi tự động 12345")
    nhap_tags(driver, "Toán,Lý,Hóa")
    nhap_ghi_chu(driver, "Đây là ghi chú tự động")
    
    remove_focus(driver)
    click_them_moi(driver)
    


    time.sleep(20)
    driver.quit()
