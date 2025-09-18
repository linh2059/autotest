import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

def get_visible_element(driver, locator):
    elements = driver.find_elements(*locator)
    for el in elements:
        if el.is_displayed():
            return el
    return None

@pytest.mark.usefixtures("driver")
def test_open_attendance_from_class(driver):
    wait = WebDriverWait(driver, 15)

    # --- Login ---
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    # --- Click vào card lớp ---
    class_card = wait.until(lambda d: get_visible_element(
        driver,
        (By.CSS_SELECTOR, "a.cursor-pointer.bg-brand-50")
    ))
    driver.execute_script("arguments[0].click();", class_card)
    print("✅ Đã click vào lớp")

    # --- Chờ đến trang lớp ---
    wait.until(EC.url_contains("/giao-vien/quan-ly-lop-hoc/Mzg"))
    print("🎉 Đã vào trang lớp học Mzg thành công")
    assert "/quan-ly-lop-hoc/Mzg" in driver.current_url

    # --- Click menu Điểm danh ---
    attendance_menu = wait.until(EC.element_to_be_clickable((
    By.XPATH,
    "//div[contains(@class,'px-8') and contains(@class,'bg-neu-200')]//a[1]"
    )))
    driver.execute_script("arguments[0].scrollIntoView(true);", attendance_menu)
    driver.execute_script("arguments[0].click();", attendance_menu)

    print("✅ Đã click menu Điểm danh")

    # --- Chờ mở trang Quản lý điểm danh ---
    wait.until(EC.url_contains("/quan-ly-diem-danh"))
    assert "/quan-ly-diem-danh" in driver.current_url
    print("🎉 Vào trang Quản lý điểm danh thành công")
