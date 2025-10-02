import pytest
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from tabulate import tabulate
from datetime import datetime, timezone, timedelta

def format_created_at(api_time_str):
    """Chuyển ISO datetime (UTC) từ API -> format UI dd/MM/yyyy HH:mm (VN timezone)"""
    if not api_time_str:
        return ""

    # parse ISO string
    dt_utc = datetime.strptime(api_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    # cộng 7 tiếng sang VN timezone
    dt_vn = dt_utc.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=7)))
    # format đúng kiểu UI
    return dt_vn.strftime("%d/%m/%Y %H:%M")


def go_to_question_bank(driver):
    wait = WebDriverWait(driver, 20)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Ngân hàng câu hỏi')]")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")


def get_api_quizzes(driver):
    """Lấy data quizzes từ performance log"""
    logs = driver.get_log("performance")
    for entry in logs:
        try:
            msg = json.loads(entry["message"])["message"]
            if msg["method"] == "Network.responseReceived":
                url = msg["params"]["response"]["url"]
                if "api/apps/quizzes" in url:
                    req_id = msg["params"]["requestId"]
                    resp = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": req_id})
                    return json.loads(resp["body"])["data"]["data"]  # ✅ list câu hỏi
        except Exception:
            continue
    return []


def get_question_table_ui(driver):
    """Lấy data câu hỏi từ bảng UI"""
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    ui_data = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            ui_data.append(cols)
    return ui_data

def map_api_to_ui(api_item):
    """Chuyển dữ liệu từ API sang format giống UI table"""
    # map độ khó
    level_map = {1: "Mức 1", 2: "Mức 2", 3: "Mức 3"}
    level_text = level_map.get(api_item.get("level", ""), "")

    return [
        str(api_item.get("unicode", "")),              # Mã định dạng
        str(api_item.get("category_name", "")),# Chủ đề (ID → có thể map sang tên nếu cần)
        api_item.get("question", ""),             # Câu hỏi
        level_text,                               # Độ khó
        # api_item.get("created_at", ""),           # Ngày tạo
        format_created_at(api_item.get("created_at", "")),  # convert ngày
        str(api_item.get("point", "")),           # Điểm
        ""                                        # Hành động (bỏ qua)
    ]


@pytest.mark.usefixtures("driver")
def test_tao_cau_hoi_complete(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    go_to_question_bank(driver)

    time.sleep(5)  # đợi API load

    # Lấy API + UI
    api_questions = get_api_quizzes(driver)
    ui_rows = get_question_table_ui(driver)

    print(f"📦 API: {len(api_questions)} câu hỏi")
    print(f"📊 UI: {len(ui_rows)} câu hỏi")
    

    assert len(api_questions) == len(ui_rows), "❌ Số lượng không khớp!"

    # So sánh từng dòng
    for i, (ui_row, api_item) in enumerate(zip(ui_rows, api_questions), start=1):
        expected = map_api_to_ui(api_item)

        # bỏ qua cột cuối (Hành động)
        ui_trimmed = ui_row[:6]

        print(f"🔎 Row {i}:")
        print(f"   UI : {ui_trimmed}")
        print(f"   API: {expected[:6]}")

        assert ui_trimmed == expected[:6], f"❌ Sai lệch dữ liệu ở row {i}"
