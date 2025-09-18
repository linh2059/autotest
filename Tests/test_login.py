# Tests/test_login.py
from Pages.login_page import LoginPage

def test_login_success(driver):
    login_page = LoginPage(driver)
    login_page.login("daotc@el.net", "123456")

    assert "quan-ly-lop-hoc" in driver.current_url, "❌ Không vào được trang quản lý lớp học"
    print("✅ Đã vào được trang quản lý lớp học!")
