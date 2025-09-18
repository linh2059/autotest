# main.py
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    # cấu hình Edge Options
    options = Options()
    # nếu muốn chạy headless (CI/CD) thì bỏ comment:
    # options.add_argument("--headless=new")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-gpu")

    # chỉ định driver path (bạn cần tải msedgedriver.exe và đặt đúng đường dẫn)
    DRIVER_PATH = r"D:\Setup\base\msedgedriver.exe"
    if not os.path.exists(DRIVER_PATH):
        print(f"❌ Không tìm thấy msedgedriver.exe tại {DRIVER_PATH}")
        sys.exit(1)

    service = Service(DRIVER_PATH)
    driver = webdriver.Edge(service=service, options=options)

    try:
        driver.get("https://school-beta.edulive.net/dang-nhap")
        print("✅ Đã mở trang login")

        wait = WebDriverWait(driver, 15)

        # nhập password
        username_input = wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//input[@class='w-full pl-10 pr-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base border rounded-lg focus:ring-2 focus:ring-primary-400 focus:border-primary-400 transition-colors border-gray-300 hover:border-gray-400']"))
        )
        username_input.send_keys("daotc@el.net")
        print("✅ Đã nhập username")
        password_input = wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//input[@class='w-full px-3 sm:px-4 py-2.5 sm:py-3 text-sm sm:text-base border rounded-lg focus:ring-2 focus:ring-primary-400 focus:border-primary-400 transition-colors pr-10 border-gray-300 hover:border-gray-400']"))
        )
        password_input.send_keys("123456")
        print("✅ Đã nhập password")

        button_input = wait.until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//button[@class='w-full py-2.5 sm:py-3 px-4 sm:px-6 bg-primary-600 text-white font-semibold text-sm sm:text-base rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-primary-600']"))
        )
        button_input.click()
        print("✅ Tiến hành đăng nhập")

        # chờ để quan sát
        time.sleep(2)

    except Exception as e:
        print("❌ Lỗi:", str(e))
    finally:
        driver.quit()
        print("🔒 Đã đóng trình duyệt")


if __name__ == "__main__":
    main()