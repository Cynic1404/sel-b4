import pytest
from selenium import webdriver


@pytest.fixture
def app(request):
    #wd = webdriver.Firefox(capabilities={"marionette": True}, executable_path="C:\Python\geckodriver.exe")
    #wd = webdriver.Firefox()
    #wd = webdriver.Edge()
    wd = webdriver.Chrome()
    wd.implicitly_wait(2)
    request.addfinalizer(wd.quit)
    return wd