# XO/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    service = Service(r"C:\Users\admin\Documents\Selenium\School_teacher\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()