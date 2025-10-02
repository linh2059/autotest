import pytest
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from tabulate import tabulate
from datetime import datetime, timezone, timedelta
from selenium.webdriver.support.ui import Select, WebDriverWait

def go_to_question_bank(driver):
    """Mở menu Ngân hàng câu hỏi và chờ trang load xong.
       (Giữ nguyên như UI thực tế của bạn)."""
    wait = WebDriverWait(driver, 20)
    # XPATH menu có thể khác — chỉnh lại nếu project bạn khác selector
    menu = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")
    ))
    # scroll + click bằng JS để tránh element bị che
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    # chờ URL chính xác (hoặc dùng url_contains nếu có params)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")


def get_pagination_info(driver):
    """Trả về số dòng + danh sách trang + trang hiện tại"""
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    row_count = len(rows)

    page_buttons = driver.find_elements(By.XPATH, "//nav//button")
    pages = []
    current_page = None

    for btn in page_buttons:
        text = btn.text.strip()
        classes = btn.get_attribute("class")

        if not text.isdigit():
            continue

        pages.append(int(text))
        if "bg-brand-900" in classes and "text-brand-50" in classes:
            current_page = int(text)

    return {
        "row_count": row_count,
        "pages": pages,
        "current_page": current_page
    }


def go_to_page(driver, page_num):
    """Click sang trang page_num"""
    wait = WebDriverWait(driver, 10)
    # tìm button chứa đúng số trang
    btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//nav//button[normalize-space(text())='{page_num}']"))
    )
    btn.click()
    time.sleep(2)  # chờ table load lại


def read_all_pages(driver):
    """Duyệt toàn bộ phân trang và in data"""
    info = get_pagination_info(driver)
    print("📄 Danh sách trang:", info["pages"])

    all_data = []

    for p in info["pages"]:
        go_to_page(driver, p)
        # sau khi click thì lấy lại row
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        page_data = [[c.text.strip() for c in r.find_elements(By.TAG_NAME, "td")] for r in rows]
        all_data.extend(page_data)

        print(f"✅ Trang {p} có {len(page_data)} dòng")

    return all_data

def get_page_size_options(driver):
    """Đọc ra danh sách số bản ghi/trang"""
    select_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[contains(@class,'select-element-custom')]"))
    )
    select = Select(select_elem)
    options = [opt.text.strip() for opt in select.options]
    return options

def set_page_size(driver, size_value):
    """
    Chọn số bản ghi/trang.
    size_value: có thể là 10, 20, 50, 100
    """
    select_elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[contains(@class,'select-element-custom')]"))
    )
    select = Select(select_elem)
    select.select_by_value(str(size_value))  # chọn theo value
    time.sleep(2)  # chờ bảng reload
    print(f"✅ Đã chọn hiển thị {size_value} / Trang")

@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    go_to_question_bank(driver)

    time.sleep(5)  # đợi API load
    # info = get_pagination_info(driver)
    # print("🔎 Số dòng hiện tại:", info["row_count"])
    # print("📄 Danh sách trang:", info["pages"])
    # print("✅ Đang ở trang:", info["current_page"])

    # all_rows = read_all_pages(driver)
    # print("📊 Tổng số dòng lấy được:", len(all_rows))

    options = get_page_size_options(driver)
    print("📌 Các lựa chọn hiển thị:", options)

    for opt in [10, 20, 50, 100]:
        set_page_size(driver, opt)
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        print(f"Trang đang hiển thị {len(rows)} dòng (mong muốn ≤ {opt})")
    # # Lấy API + UI
    # api_questions = get_api_quizzes(driver)
    # ui_rows = get_question_table_ui(driver)

    # print(f"📦 API: {len(api_questions)} câu hỏi")
    # print(f"📊 UI: {len(ui_rows)} câu hỏi")
    

    # assert len(api_questions) == len(ui_rows), "❌ Số lượng không khớp!"

    # # So sánh từng dòng
    # for i, (ui_row, api_item) in enumerate(zip(ui_rows, api_questions), start=1):
    #     expected = map_api_to_ui(api_item)

    #     # bỏ qua cột cuối (Hành động)
    #     ui_trimmed = ui_row[:6]

    #     print(f"🔎 Row {i}:")
    #     print(f"   UI : {ui_trimmed}")
    #     print(f"   API: {expected[:6]}")

    #     assert ui_trimmed == expected[:6], f"❌ Sai lệch dữ liệu ở row {i}"
