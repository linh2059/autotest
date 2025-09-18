# # class_page.py
# from selenium.webdriver.common.by import By

# class ClassPage:
#     def __init__(self, base_page):
#         self.page = base_page
#         self.wait = base_page.wait
#         self.driver = base_page.driver

#     def open_first_class(self):
#         class_card = self.wait.until(
#             lambda d: d.find_element(By.CSS_SELECTOR, "a.cursor-pointer.bg-brand-50")
#         )
#         self.page.click_js(class_card)
#         return self.driver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.base_page import BasePage

class ClassPage(BasePage):
    CLASS_CARD = (By.CSS_SELECTOR, "a.col-span-1.bg-brand-50")

    def __init__(self, driver):
        super().__init__(driver)

    def open_first_class(self):
        wait = WebDriverWait(self.driver, 15)

        # Chờ card hiển thị
        class_card = wait.until(EC.element_to_be_clickable(self.CLASS_CARD))
        class_card.click()

        # Chờ URL thay đổi sang chi tiết lớp
        wait.until(EC.url_contains("/quan-ly-lop-hoc/"))
