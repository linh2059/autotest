from selenium.webdriver.support.ui import WebDriverWait

def get_wait(driver, timeout=20):
    """
    Trả về đối tượng WebDriverWait.
    - driver: WebDriver instance
    - timeout: thời gian chờ tối đa, mặc định 20 giây
    """
    return WebDriverWait(driver, timeout)
