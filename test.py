import pytest
from selenium import webdriver


@pytest.fixture
def driver(request):
    #wd = webdriver.Firefox(capabilities={"marionette": True}, executable_path="C:\Python\geckodriver.exe")
    #wd = webdriver.Firefox()
    #wd = webdriver.Edge()
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()



def test_all_tabs(driver):
    test_login(driver)
    for el in range(len(driver.find_elements_by_xpath('//li[@id="app-"]'))):
        driver.find_elements_by_xpath('//li[@id="app-"]')[el].click()
        driver.find_element_by_xpath("//h1")
        for subtab in range(len( driver.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a"))):
            driver.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a")[subtab].click()
            driver.find_element_by_xpath("//h1")



