import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://school-beta.edulive.net/dang-nhap"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)
    yield driver
    driver.quit()


def get_visible_element(driver, locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None


def get_all_error_messages(driver):
    wait = WebDriverWait(driver, 5)
    error_elements = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//p[contains(@class,'text-red-600')]")
        )
    )
    return [e.text.strip() for e in error_elements if e.text.strip()]


# ---------------- Test Cases ----------------

def test_empty_email(driver):
    """Bỏ trống email, nhập pass"""
    input_email = get_visible_element(driver, (By.CSS_SELECTOR, "input[placeholder*='username']"))
    input_pass = get_visible_element(driver, (By.CSS_SELECTOR, "input[type='password']"))
    btn_login = get_visible_element(driver, (By.XPATH, "//button[@type='submit']"))

    input_email.clear()
    input_pass.send_keys("123456")
    btn_login.click()

    messages = get_all_error_messages(driver)
    print("⚠ Empty email:", messages)
    assert any("Vui lòng nhập thông tin đăng nhập" in m for m in messages)


def test_empty_password(driver):
    """Nhập email, bỏ trống pass"""
    input_email = get_visible_element(driver, (By.CSS_SELECTOR, "input[placeholder*='username']"))
    input_pass = get_visible_element(driver, (By.CSS_SELECTOR, "input[type='password']"))
    btn_login = get_visible_element(driver, (By.XPATH, "//button[@type='submit']"))

    input_email.send_keys("daotc@el.net")
    input_pass.clear()
    btn_login.click()

    messages = get_all_error_messages(driver)
    print("⚠ Empty password:", messages)
    assert any("Vui lòng nhập mật khẩu" in m for m in messages)


def test_invalid_email_format(driver):
    """Sai định dạng email"""
    input_email = get_visible_element(driver, (By.CSS_SELECTOR, "input[placeholder*='username']"))
    input_pass = get_visible_element(driver, (By.CSS_SELECTOR, "input[type='password']"))
    btn_login = get_visible_element(driver, (By.XPATH, "//button[@type='submit']"))

    input_email.send_keys("abc123")
    input_pass.send_keys("123456")
    btn_login.click()

    messages = get_all_error_messages(driver)
    print("⚠ Invalid email:", messages)
    assert any("Số điện thoại không đúng định dạng" in m or "Vui lòng nhập đúng định dạng" in m for m in messages)


def test_wrong_credentials(driver):
    """Sai tài khoản và mật khẩu"""
    input_email = get_visible_element(driver, (By.CSS_SELECTOR, "input[placeholder*='username']"))
    input_pass = get_visible_element(driver, (By.CSS_SELECTOR, "input[type='password']"))
    btn_login = get_visible_element(driver, (By.XPATH, "//button[@type='submit']"))

    input_email.send_keys("abc@test.com")
    input_pass.send_keys("wrongpass")
    btn_login.click()

    messages = get_all_error_messages(driver)
    print("⚠ Wrong credentials:", messages)
    assert any("Không thể kết nối đến server" in m or "Thông tin đăng nhập không chính xác" in m for m in messages)
