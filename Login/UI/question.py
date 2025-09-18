from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- Setup driver ---
service = Service(r"C:\chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 20)

# --- Hàm lấy element đang hiển thị ---
def get_visible_element(locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None

# --- Mở trang login ---
driver.get("https://school-beta.edulive.net/dang-nhap")

# --- Nhập Username ---
username_input = wait.until(lambda d: get_visible_element((By.CSS_SELECTOR, "input[placeholder*='username']")))
username_input.send_keys("daotc@el.net")

# --- Nhập Password ---
password_input = wait.until(lambda d: get_visible_element((By.CSS_SELECTOR, "input[type='password']")))
password_input.send_keys("123456")

# --- Tick Ghi nhớ đăng nhập ---
remember_button = wait.until(lambda d: get_visible_element(
    (By.XPATH, "//button[.//p[contains(text(),'Ghi nhớ đăng nhập')]]")
))
driver.execute_script("arguments[0].click();", remember_button)

# --- Click nút Đăng nhập ---
login_button = wait.until(lambda d: get_visible_element(
    (By.XPATH, "//button[contains(text(),'Đăng nhập')]")
))
login_button.click()
print("✅ Đăng nhập thành công")

# --- Chờ redirect đến trang quản lý lớp học ---
wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/quan-ly-lop-hoc"))
print("✅ Đã vào trang quản lý lớp học")

# --- Click vào card lớp ---
class_card = wait.until(lambda d: get_visible_element((
    By.CSS_SELECTOR,
    "a.cursor-pointer.bg-brand-50"
)))
driver.execute_script("arguments[0].click();", class_card)
print("✅ Đã click vào lớp")

# --- Chờ đến trang lớp cụ thể ---
wait.until(EC.url_contains("/giao-vien/quan-ly-lop-hoc/Mzg"))
print("🎉 Đã vào trang lớp học Mzg thành công")

time.sleep(3)
driver.quit()
