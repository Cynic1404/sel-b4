import pytest
from selenium import webdriver
from time import sleep


@pytest.fixture
def driver(request):
    wd = webdriver.Firefox(capabilities={"marionette": True}, executable_path="C:\Python\geckodriver.exe")
    #wd = webdriver.Firefox()
    #wd = webdriver.Edge()
    #wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_login(driver):
    driver.get("http://localhost/litecart/admin/")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("login").click()


#TASK 7
def test_all_tabs(driver):
    test_login(driver)
    for el in range(len(driver.find_elements_by_xpath('//li[@id="app-"]'))):
        driver.find_elements_by_xpath('//li[@id="app-"]')[el].click()
        driver.find_element_by_xpath("//h1")
        for subtab in range(len( driver.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a"))):
            driver.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a")[subtab].click()
            driver.find_element_by_xpath("//h1")


#TASK 8
def test_stickers(driver):
    driver.get("http://localhost/litecart/en/")
    sleep(1)
    items = driver.find_elements_by_xpath('//li[contains(@class,"product")]')
    for i in range(1,len(items)):
        assert len(items[i].find_elements_by_xpath('.//div[contains(@class, "sticker")]')) == 1

#TASK 9.1
def test_sort_country(driver):
    test_login(driver)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    countries = list(map(return_country, driver.find_elements_by_xpath("//tr[@class='row']/td[5]")))
    assert sorted(countries) == countries


def test_sort_subcountry(driver):
    test_login(driver)
    page = "http://localhost/litecart/admin/?app=countries&doc=countries"
    driver.get(page)
    megacountry = []
    for i in driver.find_elements_by_xpath("//tr[@class='row']"):
        if int(i.find_element_by_xpath("./td[6]").text) > 0:
            megacountry.append(i.find_element_by_xpath("./td[5]").text)
    for country in megacountry:
        subcountries = []
        driver.get(page)
        driver.find_element_by_link_text(country).click()
        for sub in driver.find_elements_by_xpath('//input[contains(@name, "zones") and contains(@name, "name")]'):
            subcountries.append(sub.get_attribute("value"))
            assert subcountries == sorted(subcountries)

#TASK 9.2
def test_geozones(driver):
    test_login(driver)
    page = "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones"
    driver.get(page)
    megacountry = []
    for i in driver.find_elements_by_xpath('//table[@class="dataTable"]//a[not(@title)]'):
        megacountry.append(i.text)
    for i in megacountry:
        driver.get(page)
        driver.find_element_by_link_text(i).click()
        sumcountries = list(map(return_country, driver.find_elements_by_xpath('//select[contains(@name, "zones") and contains(@name, "zone_code")]/option[@selected]')))
        assert sumcountries == sorted(sumcountries)


def return_country(x):
    return x.text

