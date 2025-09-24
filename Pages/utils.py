import time
import openpyxl
from selenium.webdriver.support.ui import WebDriverWait
from Pages.config import DEMO_MODE, DEMO_DELAY   # <--- import từ Pages/config.py

def get_wait(driver, timeout=80):
    """Trả về đối tượng WebDriverWait"""
    return WebDriverWait(driver, timeout)

def demo_pause():
    """Dừng lại một khoảng thời gian nếu đang bật DEMO_MODE"""
    if DEMO_MODE:
        time.sleep(DEMO_DELAY)
        print(f"⏸️ Demo pause for {DEMO_DELAY} seconds")

def read_test_data(file_path="data.xlsx", sheet_name="Questions"):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]
    data = []

    headers = [cell.value for cell in sheet[1]]  # lấy header ở dòng 1
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))
        # convert answers từ chuỗi -> list
        if row_data.get("answers"):
            row_data["answers"] = [a.strip() for a in row_data["answers"].split(";")]
        data.append(row_data)
    return data