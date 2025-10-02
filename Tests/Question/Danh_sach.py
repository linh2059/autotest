import pytest
from selenium import webdriver
from utils.question_bank_helper import QuestionBankHelper
from Pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def chon_chu_de(driver):
    wait = WebDriverWait(driver, 10)
    # Mở dropdown
    dropdown = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'All in')]"))
    )
    dropdown.click()

##Xóa lần lượt từng bản ghi đến hết bảng  
def delete_all_questions(driver):
    wait = WebDriverWait(driver, 10)
    count = 0

    while True:
        buttons = driver.find_elements(
            By.XPATH, "(//button[contains(@class,'btn-common btn-lighter p-2 w-fit')])[3]"
        )

        if not buttons:
            print(f"✅ Đã xoá hết toàn bộ bản ghi. Tổng số: {count}")
            break

        wait.until(EC.element_to_be_clickable(buttons[0]))
        buttons[0].click()

        modal_title = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h6[contains(text(),'Xoá câu hỏi')]"))
        )
        confirm_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Có, xoá']"))
        )
        confirm_btn.click()

        wait.until(EC.invisibility_of_element(modal_title))
        count += 1
        print(f"🗑️ Đã xoá {count} bản ghi")


        
@pytest.mark.usefixtures("driver")
def test_add_topic(driver):
    helper = QuestionBankHelper(driver)
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")
    helper.go_to_question_bank()
    chon_chu_de(driver)
    # click_first_delete_icon(driver)
    # confirm_deletion(driver)
    delete_all_questions(driver)
    time.sleep(15)
    driver.quit()
