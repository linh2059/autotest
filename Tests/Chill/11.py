import time
import json
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.login_page import LoginPage
from Tests.Chill.question import go_to_question_bank


def get_page_size_options(driver):
    """Đọc ra danh sách số bản ghi/trang"""
    select_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@class,'select-element-custom')]"))
    )
    select = Select(select_elem)
    options = [opt.text.strip() for opt in select.options]
    return options


def set_page_size(driver, size_value):
    """Chọn số bản ghi/trang"""
    select_elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[contains(@class,'select-element-custom')]"))
    )
    select = Select(select_elem)
    select.select_by_value(str(size_value))
    time.sleep(2)  # chờ bảng reload
    print(f"✅ Đã chọn hiển thị {size_value} / Trang")


def get_pagination_buttons(driver):
    """Lấy danh sách nút phân trang (số trang)"""
    buttons = driver.find_elements(By.XPATH, "//nav//button[normalize-space(text())!='']")
    return buttons


def go_to_page(driver, page_number):
    """Click sang 1 trang cụ thể"""
    btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//nav//button[normalize-space(text())='{page_number}']"))
    )
    driver.execute_script("arguments[0].click();", btn)
    time.sleep(2)  # chờ reload
    print(f"➡️ Đang ở trang {page_number}")


def read_table_data(driver):
    """Đọc dữ liệu trong bảng"""
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    data = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            data.append(cols)
    return data


def loop_all_table_data(driver):
    """Duyệt qua toàn bộ dữ liệu: theo từng page_size và từng trang"""
    all_data = []

    page_sizes = [10, 20, 50, 100]
    for size in page_sizes:
        set_page_size(driver, size)
        buttons = get_pagination_buttons(driver)
        page_numbers = [btn.text.strip() for btn in buttons if btn.text.strip().isdigit()]

        for page in page_numbers:
            go_to_page(driver, page)
            table_data = read_table_data(driver)
            print(f"📊 PageSize={size}, Page={page}, Rows={len(table_data)}")
            all_data.extend(table_data)

    return all_data

@pytest.mark.usefixtures("driver")
def test_duyet_toan_bo_bang(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    go_to_question_bank(driver)

    all_rows = loop_all_table_data(driver)
    print(f"✅ Tổng số dòng đọc được: {len(all_rows)}")