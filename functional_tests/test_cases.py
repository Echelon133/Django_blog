from django.test import TestCase
from selenium import webdriver
from page_objects.pages import (SignupPageObject,
                                HomePageObject,
                                SpecificArticlePageObject,
                                ByCategoryPageObject,
                                ByDatePageObject,
                                NotFoundPageObject)


class FunctionalTest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()


class SignupFunctionalitiesTest(FunctionalTest):
    user = {'username': 'my_username1', 
            'password': 'mypassword54321'}
    invalid_user = {'username': 'new_invalid_user',
                    'password1': 'my_new_password1',
                    'password2': 'my_other_password1'}

    def test_signup_and_add_comment(self):
        # User visits home page
        self.driver.get('http://localhost:8000/')
        home_page = HomePageObject(self.driver)

        # User goes to the signup page
        signup_page = home_page.visit_signup_page()
        
        # User creates an account
        signup_page.set_username(self.user['username'])
        signup_page.set_password1(self.user['password'])
        signup_page.set_password2(self.user['password'])
        status = signup_page.sign_up_and_return_status()
        self.assertTrue(status)
        
        # User visits main page when the account was created
        home_page = signup_page.visit_home_page()

        # User signs in
        home_page.set_username(self.user['username'])
        home_page.set_password(self.user['password'])
        home_page.login()
        
        # Compare your username to the username of logged user
        logged_username = home_page.get_logged_username()
        self.assertEqual(self.user['username'], logged_username)

        # User visits an article
        titles = home_page.get_titles_on_page()
        first_title = titles[0]
        article_page = home_page.visit_article_with_title(first_title)
        
        # User comments the article
        new_comment_text = 'my new comment'
        
        article_page.set_comment_body(new_comment_text)
        article_page.send_comment()
        
        # User checks whether the comment was posted
        comments = article_page.get_comments_as_text()
        self.assertIn(new_comment_text, comments)

    def test_signup_with_different_passwords(self):
        # User visits signup page
        self.driver.get('http://localhost:8000/signup')
        signup_page = SignupPageObject(self.driver)

        # User types in login and two different passwords
        signup_page.set_username(self.invalid_user['username'])
        signup_page.set_password1(self.invalid_user['password1'])
        signup_page.set_password2(self.invalid_user['password2'])
        
        # User tries to create an account
        status = signup_page.sign_up_and_return_status()

        # User gets correct message
        self.assertFalse(status)
        alert_msg = signup_page.get_alert_text()
        self.assertEqual(alert_msg, 'The two password fields didn\'t match.')
