# # login_page.py
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from .base_page import BasePage

# class LoginPage(BasePage):
#     URL = "https://school-beta.edulive.net/dang-nhap"

#     def login(self, email, password):
#         self.open(self.URL)

#         username_input = self.wait.until(
#             lambda d: self.get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']")) 
#         )
#         username_input.send_keys(email)

#         password_input = self.wait.until(
#             lambda d: self.get_visible_element((By.CSS_SELECTOR, "input[type='password']"))
#         )
#         password_input.send_keys(password)

#         login_button = self.wait.until(
#             lambda d: self.get_visible_element((By.XPATH, "//button[contains(text(),'Đăng nhập')]"))
#         )
#         login_button.click()
#         # demo

#         # Đợi chuyển đến trang quản lý lớp học
#         self.wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/quan-ly-lop-hoc"))
#         return self.driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class LoginPage:
    URL = "https://school-beta.edulive.net/dang-nhap"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def set_username(self, email):
        username_input = self.wait.until(
            lambda d: self.get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']")) 
        )
        username_input.clear()
        username_input.send_keys(email)

    def set_password(self, password):
        password_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.clear()
        password_input.send_keys(password)

    def click_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Đăng nhập')]"))
        )
        login_button.click()

    def get_error_message(self):
        # giả sử thông báo lỗi hiển thị dưới input
        error_element = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-form-item-explain-error"))
        )
        return error_element.text
