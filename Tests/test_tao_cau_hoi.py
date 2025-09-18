import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.login_page import LoginPage
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from Pages.utils import get_wait

# ==============================
# Data cho từng loại câu hỏi
# ==============================
question_data = [
    ("mot_lua_chon", {
        "noi_dung": "Chọn đáp án đúng: 2 + 2 = ?",
        "dap_an": ["2", "3", "4"],
        "dung": "4"
    }),
    ("dien_khuyet", {
        "noi_dung": "1 + 1 = ___",
        "dap_an": ["2"]
    }),
    ("ghep_noi", {
        "noi_dung": "Ghép cặp đúng",
        "dap_an": [("Hà Nội", "Việt Nam"), ("Tokyo", "Nhật Bản")]
    }),
    ("tu_luan", {
        "noi_dung": "Em hãy viết đoạn văn ngắn tả ngôi trường của em.",
        "dap_an": None
    }),
]

# ==============================
# Fixture mở Chrome
# ==============================
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# ==============================
# Các hàm thao tác chung
# ==============================
def go_to_question_bank(driver):
    wait = get_wait(driver)
    menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Ngân hàng câu hỏi']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu)
    driver.execute_script("arguments[0].click();", menu)
    wait.until(EC.url_to_be("https://school-beta.edulive.net/giao-vien/ngan-hang-cau-hoi"))
    print("✅ Vào trang Ngân hàng câu hỏi")

def open_add_topic_modal(driver):
    wait = get_wait(driver)
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Tạo câu hỏi mới')]"))))
    driver.execute_script("arguments[0].click();", wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='text-sm']"))))
    print("✅ Mở modal tạo câu hỏi mới")

def select_parent_option(driver, parent_title):
    wait = get_wait(driver)
    parent_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"button[title='{parent_title}']")))
    driver.execute_script("arguments[0].click();", parent_btn)
    time.sleep(1)
    print(f"✅ Chọn chủ đề cha: {parent_title}")

def chon_muc_do(driver, level: int):
    wait = get_wait(driver)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//div[contains(@class,'col-span-1 flex flex-col gap-1.5')]//button)[{level}]")))
    driver.execute_script("arguments[0].click();", button)
    print(f"✅ Chọn mức độ {level}")

def chon_loai_cau_hoi(driver, loai):
    if loai == "mot_lua_chon":
        css = "button[title='Một lựa chọn']"
    elif loai == "dien_khuyet":
        css = "button[title='Điền vào chỗ trống']"
    elif loai == "ghep_noi":
        css = "button[title='Ghép nối']"
    elif loai == "tu_luan":
        css = "button[title='Tự luận']"
    else:
        raise ValueError(f"Loại câu hỏi không hỗ trợ: {loai}")

    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css))
    ).click()

def nhap_noi_dung(driver, text):
    text_area = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Nhập nội dung câu hỏi']"))
    )
    text_area.clear()
    text_area.send_keys(text)

def nhap_dap_an(driver, loai, dap_an, dung=None):
    if loai == "mot_lua_chon":
        for i, val in enumerate(dap_an):
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"(//input[@placeholder='Nhập đáp án'])[{i+1}]"))
            )
            input_box.clear()
            input_box.send_keys(val)

        # chọn đáp án đúng (theo tham số dung)
        correct = dung if dung else dap_an[0]
        correct_radio = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[contains(.,'{correct}')]/preceding-sibling::input[@type='radio']"))
        )
        driver.execute_script("arguments[0].click();", correct_radio)

    elif loai == "dien_khuyet":
        # nếu có ô nhập đáp án đúng thì điền
        for i, val in enumerate(dap_an):
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"(//input[@placeholder='Nhập đáp án đúng'])[{i+1}]"))
            )
            input_box.clear()
            input_box.send_keys(val)

    elif loai == "ghep_noi":
        for i, (left, right) in enumerate(dap_an):
            left_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"(//input[@placeholder='Thuộc tính A'])[{i+1}]"))
            )
            right_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"(//input[@placeholder='Thuộc tính B'])[{i+1}]"))
            )
            left_box.clear()
            right_box.clear()
            left_box.send_keys(left)
            right_box.send_keys(right)

    elif loai == "tu_luan":
        # Tự luận không có đáp án
        pass

def save_question(driver):
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Lưu')]"))
    ).click()
    time.sleep(2)

def check_question_exists(driver, text):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[contains(.,'{text}')]"))
        )
        return True
    except:
        return False

# ==============================
# Test parametrize
# ==============================
@pytest.mark.parametrize("loai,data", question_data)
def test_tao_cau_hoi(driver, loai, data):
    login(driver, "daotc@el.net", "123456")   # 👉 sửa email/password thật ở đây
    open_question_bank(driver)
    open_create_modal(driver)
    chon_loai_cau_hoi(driver, loai)
    nhap_noi_dung(driver, data["noi_dung"])
    nhap_dap_an(driver, loai, data["dap_an"], data.get("dung"))
    save_question(driver)

    assert check_question_exists(driver, data["noi_dung"])
