import pytest
from selenium import webdriver



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome("C:\Python\chromedriver.exe")
    request.addfinalizer(wd.quit)
    return wd


def test_example(driver):
    driver.get("https://msk.software-testing.ru/")
    driver.find_element_by_xpath("//a[@href='http://selenium2.ru/']").click()

