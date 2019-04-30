import random
import string


def random_phone():
    return "+" + str(random.randint(1, 10)) + "-" + "".join([random.choice(string.digits) for i in range(3)]) + "-" + "".join([random.choice(string.digits) for i in range(3)]) + "-" + "".join([random.choice(string.digits) for i in range(2)]) + "-" + "".join([random.choice(string.digits) for i in range(2)])


def fill_registartion_forms(driver, user):
    driver.find_element_by_name("firstname").send_keys(user.name)
    driver.find_element_by_name("lastname").send_keys(user.lastname)
    driver.find_element_by_name("address1").send_keys(user.address)
    driver.find_element_by_name("city").send_keys(user.city)
    driver.find_element_by_name("email").send_keys(user.email)
    driver.find_element_by_name("postcode").send_keys(user.postcode)
    driver.find_element_by_name("phone").send_keys(user.phone)
    driver.find_element_by_name("password").send_keys(user.password)
    driver.find_element_by_name("confirmed_password").send_keys(user.password)


def login(driver, email, password):
    driver.get("http://localhost/litecart/en/")
    driver.find_element_by_name("email").send_keys(email)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("login").click()


def logout(driver):
    driver.find_element_by_xpath("//div[@class='content']//a[contains(text(),'Logout')]").click()


def return_country(x):
    return x.text


def check_grey_color(color):
    if int(color[0])==int(color[1])==int(color[2]):
        return True


def check_red_color(color):
    if int(color[1])==int(color[2])==0:
        return True


def random_email():
    symbols = string.ascii_letters + string.digits
    return "".join([random.choice(symbols) for i in range(random.randrange(1,10))])+"@"+ "".join([random.choice(symbols) for i in range(random.randrange(1,10))]) + random.choice([".ru", ".com"])


def random_password(maxlen):
    symbols = string.ascii_letters+string.digits
    return "".join(random.choice(symbols) for i in range(random.randrange(5, maxlen)))