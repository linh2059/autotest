# login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://school-beta.edulive.net/dang-nhap"

    def login(self, email, password):
        self.open(self.URL)

        username_input = self.wait.until(
            lambda d: self.get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']"))
        )
        username_input.send_keys(email)

        password_input = self.wait.until(
            lambda d: self.get_visible_element((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.send_keys(password)

        login_button = self.wait.until(
            lambda d: self.get_visible_element((By.XPATH, "//button[contains(text(),'Đăng nhập')]"))
        )
        login_button.click()

        # Đợi chuyển đến trang quản lý lớp học
        self.wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/quan-ly-lop-hoc"))
        return self.driver
