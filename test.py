from time import sleep
from functions import *
from product import Product
from new_user import NewUser


def test_login(app):
    app.get("http://localhost/litecart/admin/")
    app.find_element_by_name("username").send_keys("admin")
    app.find_element_by_name("password").send_keys("admin")
    app.find_element_by_name("login").click()


#TASK 7
def test_all_tabs(app):
    test_login(app)
    for el in range(len(app.find_elements_by_xpath('//li[@id="app-"]'))):
        app.find_elements_by_xpath('//li[@id="app-"]')[el].click()
        app.find_element_by_xpath("//h1")
        for subtab in range(len(app.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a"))):
            app.find_elements_by_xpath('//li[@id="app-"]')[el].find_elements_by_xpath("./ul//a")[subtab].click()
            app.find_element_by_xpath("//h1")


#TASK 8
def test_stickers(app):
    app.get("http://localhost/litecart/en/")
    sleep(1)
    items = app.find_elements_by_xpath('//li[contains(@class,"product")]')
    for i in range(1,len(items)):
        assert len(items[i].find_elements_by_xpath('.//div[contains(@class, "sticker")]')) == 1

#TASK 9.1
def test_sort_country(app):
    test_login(app)
    app.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    countries = list(map(return_country, app.find_elements_by_xpath("//tr[@class='row']/td[5]")))
    assert sorted(countries) == countries


def test_sort_subcountry(app):
    test_login(app)
    page = "http://localhost/litecart/admin/?app=countries&doc=countries"
    app.get(page)
    megacountry = []
    for i in app.find_elements_by_xpath("//tr[@class='row']"):
        if int(i.find_element_by_xpath("./td[6]").text) > 0:
            megacountry.append(i.find_element_by_xpath("./td[5]").text)
    for country in megacountry:
        subcountries = []
        app.get(page)
        app.find_element_by_link_text(country).click()
        for sub in app.find_elements_by_xpath('//input[contains(@name, "zones") and contains(@name, "name")]'):
            subcountries.append(sub.get_attribute("value"))
            assert subcountries == sorted(subcountries)

#TASK 9.2
def test_geozones(app):
    test_login(app)
    page = "http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones"
    app.get(page)
    megacountry = []
    for i in app.find_elements_by_xpath('//table[@class="dataTable"]//a[not(@title)]'):
        megacountry.append(i.text)
    for i in megacountry:
        app.get(page)
        app.find_element_by_link_text(i).click()
        sumcountries = list(map(return_country, app.find_elements_by_xpath('//select[contains(@name, "zones") and contains(@name, "zone_code")]/option[@selected]')))
        assert sumcountries == sorted(sumcountries)

#TASK 10
def test_product(app):
    app.implicitly_wait(5)
    app.get("http://localhost/litecart/en/")
    item = app.find_element_by_xpath('//li[contains(@class,"product")]')
    title = item.find_element_by_xpath(".//div[@class='name']").text
    try:
        regular_price = item.find_element_by_css_selector('.price').text
        product = Product(title=title, regular_price=regular_price)
        color_regular = app.find_element_by_css_selector('.price').value_of_css_property("color")[5:-4].split(",")
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
    assert product.title == app.find_element_by_xpath('//h1[@class="title"]').text

    if sale:
        regular_price_on_page = app.find_element_by_css_selector('.regular-price')
        assert product.regular_price == regular_price_on_page.text
        deal_price_on_page = app.find_element_by_css_selector('.campaign-price')
        assert product.deal_price == deal_price_on_page.text
        assert regular_price_on_page.value_of_css_property("font-size") < deal_price_on_page.value_of_css_property("font-size")
        assert (regular_price_on_page.value_of_css_property("text-decoration")).split()[0] == 'line-through'

    else:
        assert product.regular_price == app.find_element_by_xpath('//span[@itemprop="price"]').text


#TASK 11
def test_registration(app):
    app.get("http://localhost/litecart/en/")
    app.find_element_by_xpath("//a[contains(text(),'New customers click here')]").click()
    email = random_email()
    phone = random_phone()
    password = random_password(10)
    new_user = NewUser("Bob", "Thorton", "3639 Haven Ave", "Menlo Park", 94025, email, phone, password)
    fill_registartion_forms(app, new_user)
    app.find_element_by_name("create_account").click()
    logout(app)
    login(app, new_user.email, new_user.password)
    logout(app)


