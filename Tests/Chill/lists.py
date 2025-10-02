# Tests/test_question_bank_compare.py
import pytest
import time
import json
from datetime import datetime, timezone, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage

# --------------------------
# GHI CHÚ CHUNG (important)
# - Yêu cầu: trong conftest.py fixture `driver` phải bật performance logging:
#     options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
#   và driver phải được tạo bằng: webdriver.Chrome(service=service, options=options)
# - Test này lấy response JSON từ Chrome DevTools log (performance),
#   không gọi API trực tiếp. Vì vậy phải đảm bảo request / response đã diễn ra trước khi lấy log.
# - UI table columns (theo yêu cầu):
#     0: Mã định dạng
#     1: Chủ đề
#     2: Câu hỏi
#     3: Độ khó
#     4: Ngày tạo (UI format: dd/MM/YYYY HH:MM, timezone VN = UTC+7)
#     5: Điểm
#     6: Hành động (bỏ qua so sánh)
# - API trả `created_at` là ISO UTC như: 2025-09-26T07:04:11.000000Z
#   cần convert sang "26/09/2025 14:04" để so sánh với UI.
# --------------------------


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


def get_api_quizzes_from_performance(driver, api_path="/api/apps/quizzes"):
    """
    Lấy response JSON của API quizzes từ performance logs.
    Trả về list các item (data.data).
    Ghi chú:
      - Vì Chrome có thể xoá resource nhanh, nên gọi hàm này ngay sau khi trang load xong.
      - Hàm sẽ tìm event Network.responseReceived có url chứa api_path,
        lấy requestId và gọi CDP Network.getResponseBody để lấy body.
    """
    try:
        logs = driver.get_log("performance")
    except Exception as e:
        print("⚠️ Không lấy được performance logs:", e)
        return []

    for entry in logs:
        try:
            msg = json.loads(entry["message"])["message"]
            # quan tâm event responseReceived chứa URL + requestId
            if msg.get("method") == "Network.responseReceived":
                resp = msg.get("params", {}).get("response", {})
                url = resp.get("url", "")
                if api_path in url:
                    request_id = msg["params"]["requestId"]
                    # Lấy response body qua CDP
                    try:
                        resp_body = driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
                    except Exception as e:
                        # Thường gặp lỗi "No resource with given identifier found" nếu request expired -> bỏ qua
                        print("⚠️ Không lấy được response body (resource expired):", e)
                        continue

                    # resp_body có keys: 'body' (str) và 'base64Encoded' (bool)
                    body_text = resp_body.get("body", "")
                    try:
                        data = json.loads(body_text)
                        # theo cấu trúc sample: { result: true, data: { current_page:..., data: [ ... ] }, ... }
                        # kiểm tra tồn tại path data.data
                        quizzes = data.get("data", {}).get("data", [])
                        print(f"📌 Lấy được API quizzes từ: {url} (count={len(quizzes)})")
                        return quizzes
                    except Exception as e:
                        print("⚠️ JSON parse error:", e)
                        continue
        except Exception:
            # skip các log không parse được
            continue

    print("⚠️ Không tìm thấy response quizzes trong performance logs")
    return []


def get_question_table_ui(driver):
    """
    Đọc bảng UI (tbody rows) và trả về list of lists:
    mỗi row là list các cell text (đã strip).
    Bỏ qua rows rỗng/rows expand nếu cần.
    """
    # chọn tr có td (bỏ các tr rỗng / spacer)
    rows = driver.find_elements(By.XPATH, "//table/tbody/tr[td]")
    ui_data = []
    for row in rows:
        cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
        # nếu UI rút gọn câu hỏi sẽ có '...' — giữ nguyên để so sánh theo luật bên dưới
        if cols:
            ui_data.append(cols)
    print(f"📋 Lấy được {len(ui_data)} rows từ UI")
    return ui_data


def format_created_at(api_time_str):
    """
    Convert API ISO UTC (e.g. 2025-09-26T07:04:11.000000Z)
    -> UI format dd/MM/YYYY HH:MM in Vietnam timezone (UTC+7), no seconds.
    Trả về chuỗi str hoặc "" nếu parse lỗi.
    """
    if not api_time_str:
        return ""
    try:
        # parse ISO with microseconds and trailing Z
        dt_utc = datetime.strptime(api_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        # có thể API trả khác dạng, thử parse ngắn hơn (without microseconds)
        try:
            dt_utc = datetime.strptime(api_time_str, "%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            return ""
    # attach tz and convert to UTC+7
    dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    dt_vn = dt_utc.astimezone(timezone(timedelta(hours=7)))
    return dt_vn.strftime("%d/%m/%Y %H:%M")  # dd/MM/YYYY HH:MM


def map_api_item_to_ui_row(api_item, level_map=None):
    """
    Map 1 API item -> expected UI row (list of 7 values) to compare.
    level_map: optional dict to map numeric level -> Vietnamese text
    Returns list: [id, category_display, question, level_text, created_at_formatted, point, ""]
    - category_display: by default use quiz_category_id (string). If you want name, need extra mapping.
    """
    if level_map is None:
        level_map = {1: "Mức 1", 2: "Mức 2", 3: "Mức 3"}  # adjust to your UI naming (your UI used "Mức 1" earlier)
        # NOTE: you told earlier UI used "Mức 1" etc. adjust if UI uses "Dễ/Trung bình/Khó"

    # category: API provides quiz_category_id (numeric). If UI shows name, you must map ids->names before compare.
    category_display = str(api_item.get("quiz_category_id", ""))

    return [
        str(api_item.get("unicode", "")),                     # Mã định dạng
        api_item.get("category_name", ""),# Chủ đề (ID → có thể map sang tên nếu cần)
        api_item.get("question", ""),                    # Câu hỏi (full text from API)
        level_map.get(api_item.get("level", ""), ""),    # Độ khó mapped (ví dụ "Mức 1")
        format_created_at(api_item.get("created_at", "")),# Ngày tạo converted to UI format
        str(api_item.get("point", "")),                  # Điểm
        ""                                               # Hành động (bỏ trống để skip)
    ]


def compare_ui_api(ui_data, api_items):
    """
    So sánh 2 lists:
    - ui_data: list of lists (each row cells)
    - api_items: list of API items (raw JSON objects)
    Rule:
      - So sánh 6 cột đầu (bỏ cột hành động)
      - Cột Câu hỏi (index 2): nếu UI chứa '...' ở cuối -> so sánh prefix (startsWith),
        nếu không -> strict equality.
      - Ngày tạo: API -> convert -> dd/MM/YYYY HH:MM then compare
      - Chủ đề: hiện đang so sánh bằng quiz_category_id (ID). Nếu UI hiển thị tên, cần mapping
    Trả về list of mismatch messages (empty nếu tất cả khớp).
    """
    mismatches = []

    # tạo expected rows list từ api_items
    expected_rows = [map_api_item_to_ui_row(item) for item in api_items]

    # compare length first
    if len(ui_data) != len(expected_rows):
        mismatches.append(f"Số lượng rows khác nhau: UI={len(ui_data)} vs API={len(expected_rows)}")
        # vẫn ta tiếp tục so sánh zip để lấy chi tiết khác (để debug)
    
    total = min(len(ui_data), len(expected_rows))
    for i in range(total):
        ui_row = ui_data[i]
        api_row = expected_rows[i]

        # compare first 6 columns only
        for col_idx in range(6):
            ui_val = ui_row[col_idx] if col_idx < len(ui_row) else ""
            api_val = api_row[col_idx] if col_idx < len(api_row) else ""

            # Column-specific handling
            if col_idx == 2:
                # Câu hỏi (index 2)
                if ui_val.endswith("..."):
                    prefix = ui_val[:-3]
                    if not api_val.startswith(prefix):
                        mismatches.append(
                            f"Row {i+1} Câu hỏi prefix mismatch: UI='{ui_val}' | API-starts='{api_val[:len(prefix)+20]}...'"
                        )
                else:
                    if ui_val != api_val:
                        mismatches.append(f"Row {i+1} Câu hỏi khác: UI='{ui_val}' | API='{api_val}'")
            elif col_idx == 4:
                # Ngày tạo: api_val đã được format trong map_api_item_to_ui_row()
                if ui_val != api_val:
                    mismatches.append(f"Row {i+1} Ngày tạo khác: UI='{ui_val}' | API-formatted='{api_val}'")
            else:
                # strict compare for other columns (id, category, level, point)
                if ui_val != api_val:
                    col_names = ["Mã", "Chủ đề", "Câu hỏi", "Độ khó", "Ngày tạo", "Điểm"]
                    mismatches.append(f"Row {i+1} {col_names[col_idx]} khác: UI='{ui_val}' | API='{api_val}'")

    return mismatches


# --------------------------
# Actual pytest test that ties everything together
# --------------------------
@pytest.mark.usefixtures("driver")
def test_compare_question_bank_ui_vs_api(driver):
    """
    Test flow:
    1. login
    2. navigate to question bank
    3. wait & collect performance logs
    4. parse API quizzes response
    5. collect UI table rows
    6. compare via compare_ui_api()
    """
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    # (optional) small wait to ensure login complete; adjust as needed
    time.sleep(1)

    # vào trang Ngân hàng câu hỏi
    go_to_question_bank(driver)

    # ĐỢI API gọi -> nhỏ hơn sleep cố định là tốt nhưng ở đây dùng sleep để đơn giản
    # Bạn có thể thay bằng WebDriverWait chờ spinner biến mất / hoặc chờ table có rows
    time.sleep(3)

    # 1) LẤY API từ performance logs
    api_items = get_api_quizzes_from_performance(driver)
    assert api_items, "❌ Không lấy được API quizzes từ performance logs"

    # 2) LẤY UI table rows
    ui_rows = get_question_table_ui(driver)
    assert ui_rows, "❌ Không tìm thấy rows trong UI table"

    # 3) SO SÁNH
    mismatches = compare_ui_api(ui_rows, api_items)

    # Print diagnostic info
    if mismatches:
        print("❌ Có mismatch sau khi so sánh UI <-> API:")
        for m in mismatches:
            print("   -", m)
    else:
        print("✅ UI và API khớp theo rules đã định")

    # Final assertion: fail test nếu có mismatch
    assert not mismatches, "UI và API không khớp (xem log để biết chi tiết)"

