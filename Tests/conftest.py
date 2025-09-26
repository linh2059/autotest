# Tests/conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture(scope="function")
def driver():
    
    service = Service(r"C:\chromedriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()
