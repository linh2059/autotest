# # base_page.py
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

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# class BasePage:
#     """Class cơ sở cho tất cả Page Object.
#        Cung cấp các hàm tiện ích: click, fill input, tìm element, bỏ focus, đợi URL...
#        Giúp code gọn và dễ maintain."""

#     def __init__(self, driver, timeout=20):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, timeout)

#     # ------------------- Các hàm thao tác element -------------------
#     def find(self, locator):
#         """Chờ và trả về element"""
#         return self.wait.until(EC.presence_of_element_located(locator))

#     def click(self, locator):
#         """Chờ element có thể click và click"""
#         el = self.wait.until(EC.element_to_be_clickable(locator))
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
#         self.driver.execute_script("arguments[0].click();", el)

#     def fill(self, locator, text):
#         """Nhập text vào input/textarea"""
#         el = self.wait.until(EC.visibility_of_element_located(locator))
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
#         el.clear()
#         el.send_keys(text)

#     # ------------------- Các hàm tiện ích khác -------------------
#     def remove_focus(self):
#         """Bỏ focus khỏi input/textarea trước khi submit"""
#         self.driver.execute_script("document.activeElement.blur();")
#         print("✅ Đã bỏ focus khỏi input")

#     def wait_for_url(self, url):
#         """Chờ cho đến khi URL thay đổi giống như mong muốn"""
#         self.wait.until(EC.url_to_be(url))
