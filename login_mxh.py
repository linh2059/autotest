import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- Setup driver ---
service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 20)

def get_visible_element(driver, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located(locator))

def get_visible(locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None

def test_login_success(driver):
    #1 Mở trang web 
    driver.get('https://social-beta.edulive.net/sign-in')

    #2 Nhập tên đăng nhập
    username_input = get_visible_element(driver, (By.NAME, 'username'))
    username_input.send_keys('tchoaaa@el.net')

    #3 Nhập mật khẩu
    password_input = get_visible_element(driver, (By.NAME, 'password'))
    password_input.send_keys('123456')

    #4 Click nút đăng nhập
    login_button = get_visible_element(driver, (By.XPATH, "(//button[@class='button-modal more w-full mt-5'])[1]"))
    login_button.click()

    #5 Kiểm tra đăng nhập thành công
    # try:
    #     # menu_user_btn = wait.until(lambda d: get_visible(
    #     #     (By.XPATH, "(//*[name()='svg'][@class='tabler-icon tabler-icon-caret-down-filled '])[1]")
    #     # ))
    #     menu_user_btn = WebDriverWait(driver, 5).until(
    #         EC.presence_of_element_located((By.ID, "User Avatar"))
    #     )
    #     print("✅ menu_user button có trên trang")
    # except TimeoutException:
    #     print("❌ Không tìm thấy menu_user button")
    
    # def open_add_modal(driver):
    #     wait = WebDriverWait(driver, 20)
    #     driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button-common !bg-transparent !text-inherit !border-0 !p-0 !m-0 !shadow-none !rounded-none']//*[name()='svg']"))))
    # print("✅ Mở modal tạo câu hỏi mới")
   
    remember_button = wait.until(lambda d: get_visible(
        (By.XPATH, "//span[contains(text(),'Thư viện của tôi')]")
    ))
    driver.execute_script("arguments[0].click();", remember_button)  # click an toàn bằng JS
time.sleep(5)
driver.quit()
