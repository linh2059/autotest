# base_page.py
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def get_visible_element(self, locator):
        """Trả về element hiển thị được"""
        elements = self.driver.find_elements(*locator)
        for el in elements:
            if el.is_displayed():
                return el
        return None

    def click_js(self, element):
        """Click an toàn bằng JavaScript"""
        self.driver.execute_script("arguments[0].click();", element)

    def open(self, url):
        """Mở URL"""
        self.driver.get(url)

    def current_url(self):
        return self.driver.current_url
