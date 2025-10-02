# Tests/conftest.py
import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import allure

@pytest.fixture(scope="function")
def driver(request):
    options = webdriver.ChromeOptions()

    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })

    service = Service(r"C:\Users\admin\Documents\Selenium\Setup\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    
    # Sau khi chạy xong test
    if request.node.rep_call.failed:
        # Tạo folder screenshots nếu chưa có
        os.makedirs("screenshots", exist_ok=True)

        screenshot_path = f"screenshots/{request.node.name}.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved: {screenshot_path}")

        # Gắn screenshot vào Allure
        allure.attach.file(
            screenshot_path,
            name=f"Screenshot_{request.node.name}",
            attachment_type=allure.attachment_type.PNG
        )
        
    driver.quit()

# Hook để bắt trạng thái test (pass/fail)
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


# Hook để gắn screenshot link vào pytest-html report
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_row(report, cells):
    if report.when == "call" and report.failed:
        screenshot_path = f"screenshots/{report.nodeid.split('::')[-1]}.png"
        if os.path.exists(screenshot_path):
            cells.insert(
                1,
                f"<a href='{screenshot_path}' target='_blank'>📸 Screenshot</a>"
            )