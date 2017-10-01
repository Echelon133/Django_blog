from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager

from locators.locators import PageWithLoginLocators


class BasePageObject:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def get_page_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def visit_home_page(self):
        homepage_link = self.find_element(*PageWithLoginLocators.homepage_link)
        homepage_link.click()
        # return HomePageObject

    def get_description_text(self):
        description = self.find_element(*PageWithLoginLocators.description)
        return description.text


class BasePageObjectWithLogin(BasePageObject):

    def set_username(self, username):
        login_field = self.find_element(*PageWithLoginLocators.username_field)
        login_field.send_keys(username)

    def set_password(self, password):
        password_field = self.find_element(*PageWithLoginLocators.password_field)
        password_field.send_keys(password)

    def login(self):
        login_btn = self.find_element(*PageWithLoginLocators.login_button)
        login_btn.click()

    def logout(self):
        logout_link = self.find_element(*PageWithLoginLocators.logout_link)
        logout_link.click()

    def get_logged_username(self):
        logged_as = self.find_element(*PageWithLoginLocators.logged_as_text)
        # 'Logged in as XYZ'. Slicing from 13 letter gives username
        username = logged_as.text[13:]
        return username

    def visit_signup_page(self):
        signup_link = self.find_element(*PageWithLoginLocators.signup_link)
        # return SignupPageObject(self.driver)
        
        