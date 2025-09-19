import time
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