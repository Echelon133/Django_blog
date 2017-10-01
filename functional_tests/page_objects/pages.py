from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from contextlib import contextmanager

from locators.locators import PageWithLoginLocators
from locators.locators import SignupPageLocators
from locators.locators import ListedArticlesPageLocators


class BasePageObject:

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def get_page_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def visit_home_page(self):
        homepage_link = self.find_element(*PageWithLoginLocators.homepage_link)
        homepage_link.click()
        return HomePageObject

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
        return SignupPageObject(self.driver)


class ListedArticlesPageObject(BasePageObjectWithLogin):
    
    def get_titles_on_page(self):
        titles = self.find_elements(*ListedArticlesPageLocators.article_titles)
        all_titles = [title.text for title in titles]
        return all_titles

    def visit_article_with_title(self, title):
        articles = self.find_elements(*ListedArticlesPageLocators.article_links)
        for article in articles:
            if article.text == title:
                article.click()
                return SingleArticlePageObject(self.driver)
            else:
                return self

    def visit_next_page(self):
        paginator_links = self.find_elements(*ListedArticlesPageLocators.paginator_links)
        for link in paginator_links:
            if link.text == 'Next Page':
                link.click()
                return self

    def visit_previous_page(self):
        paginator_links = self.find_elements(*ListedArticlesPageLocators.paginator_links)
        for link in paginator_links:
            if link.text == 'Previous Page':
                link.click()
                return self
    

class SignupPageObject(BasePageObject):
    
    def set_username(self, username):
        username_field = self.find_element(*SignupPageLocators.username_field)
        username_field.send_keys(username)

    def set_password1(self, password1):
        password1_field = self.find_element(*SignupPageLocators.password1_field)
        password1_field.send_keys(password1)

    def set_password2(self, password2):
        password2_field = self.find_element(*SignupPageLocators.password2_field)
        password2_field.send_keys(password2)

    def sign_up_and_return_status(self):
        signup_button = self.find_element(*SignupPageLocators.signup_button)
        signup_button.click()
        # clicking on this button reloads the page
        self.driver.implicitly_wait(5)
        alert = self.find_element(*SignupPageLocators.alert_text)
        alert_text = alert.text
        if alert_text == 'User creation successful. You can log in now.':
            return True
        else:
            return False


class HomePageObject(ListedArticlesPageObject):
    pass


class SingleArticlePageObject(BasePageObjectWithLogin):
    pass


class ByCategoryPageObject(ListedArticlesPageObject):
    pass


class ByDatePageObject(ListedArticlesPageObject):
    pass


class NotFoundPageObject(BasePageObjectWithLogin):
    pass