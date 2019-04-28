import pytest
from selenium import webdriver
from time import sleep
from product import Product



@pytest.fixture
def driver(request):
    #wd = webdriver.Firefox(capabilities={"marionette": True}, executable_path="C:\Python\geckodriver.exe")
    #wd = webdriver.Firefox()
    #wd = webdriver.Edge()
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
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

#TASK 10
def test_product(driver):
    driver.implicitly_wait(5)
    driver.get("http://localhost/litecart/en/")
    item = driver.find_element_by_xpath('//li[contains(@class,"product")]')
    title = item.find_element_by_xpath(".//div[@class='name']").text
    try:
        regular_price = item.find_element_by_css_selector('.price').text
        product = Product(title=title, regular_price=regular_price)
        color_regular = driver.find_element_by_css_selector('.price').value_of_css_property("color")[5:-4].split(",")
        assert check_grey_color(color_regular)
        sale = False
    except:
        regular_price = item.find_element_by_css_selector('.regular-price').text
        deal_price = item.find_element_by_css_selector('.campaign-price').text
        product = Product(title=title, regular_price=regular_price, deal_price=deal_price)
        color_regular = item.find_element_by_css_selector('.regular-price').value_of_css_property("color")[5:-4].split(",")
        color_deal = item.find_element_by_css_selector('.campaign-price').value_of_css_property("color")[5:-4].split(",")
        assert check_red_color(color_deal)
        assert check_grey_color(color_regular)
        assert item.find_element_by_css_selector('.regular-price').value_of_css_property("font-size") < item.find_element_by_css_selector('.campaign-price').value_of_css_property("font-size")
        assert (item.find_element_by_css_selector('.regular-price').value_of_css_property("text-decoration")).split()[0] == 'line-through'
        sale = True

    item.click()
    assert product.title == driver.find_element_by_xpath('//h1[@class="title"]').text

    if sale:
        regular_price_on_page = driver.find_element_by_css_selector('.regular-price')
        assert product.regular_price == regular_price_on_page.text
        deal_price_on_page = driver.find_element_by_css_selector('.campaign-price')
        assert product.deal_price == deal_price_on_page.text
        assert regular_price_on_page.value_of_css_property("font-size") < deal_price_on_page.value_of_css_property("font-size")
        assert (regular_price_on_page.value_of_css_property("text-decoration")).split()[0] == 'line-through'

    else:
        assert product.regular_price == driver.find_element_by_xpath('//span[@itemprop="price"]').text


def return_country(x):
    return x.text

def check_grey_color(color):
    if int(color[0])==int(color[1])==int(color[2]):
        return True

def check_red_color(color):
    if int(color[1])==int(color[2])==0:
        return True