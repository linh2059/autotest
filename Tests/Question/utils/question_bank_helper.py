from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class QuestionBankHelper:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def go_to_question_bank(self):
        menu = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]"))
        )
        self.driver.execute_script("arguments[0].click();", menu)
        self.wait.until(
            EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi")
        )
        print("✅ Vào trang Ngân hàng câu hỏi")

    def open_add_topic_modal(self):
        add_topic_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm chủ đề')]"))
        )
        self.driver.execute_script("arguments[0].click();", add_topic_btn)
        print("✅ Đã click nút Thêm chủ đề")

    def new_topic(self, ten_chu_de):
        modal_input = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Nhập tên chủ đề']"))
        )
        modal_input.click()
        modal_input.clear()
        modal_input.send_keys(ten_chu_de)
        self.driver.execute_script("arguments[0].blur();", modal_input)  # trigger validate
        return modal_input

    def submit_new_topic(self):
        save_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Thêm mới')]"))
        )
        self.driver.execute_script("arguments[0].click();", save_btn)
        print("✅ Đã click nút Lưu")

    def get_error_message(self):
        error_el = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".elements-custom.error-element-custom"))
        )
        return error_el.text.strip()
