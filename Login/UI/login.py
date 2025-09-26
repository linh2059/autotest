import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from Pages.login_page import LoginPage

import pytest
from Pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestLoginValidate:

    def test_empty_username_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.click_login()

        error_msg = login_page.get_error_message()
        assert "Vui lòng nhập tên đăng nhập" in error_msg or "Vui lòng nhập mật khẩu" in error_msg

    def test_empty_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.set_username("daotc@el.net")
        login_page.click_login()

        error_msg = login_page.get_error_message()
        assert "Vui lòng nhập mật khẩu" in error_msg

    def test_wrong_username_password(self, driver):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.set_username("saiuser@el.net")
        login_page.set_password("saimatkhau")
        login_page.click_login()

        error_msg = login_page.get_error_message()
        assert "Sai tên đăng nhập hoặc mật khẩu" in error_msg

