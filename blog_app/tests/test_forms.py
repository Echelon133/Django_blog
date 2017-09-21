from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore
from django.test.client import RequestFactory
from django.http import QueryDict
from blog_app.forms import UserLoginForm, UserSignupForm, CommentForm
from blog_app.models import User, Comment, Article
from django.core.exceptions import ValidationError


class CommentFormTest(TestCase):
    
    def test_comment_form_has_correct_restrictions(self):
        comment_form = CommentForm()
        self.assertIn('maxlength="500"', comment_form.as_p())
        self.assertIn('required', comment_form.as_p())

    def test_comment_form_fails_with_incorrect_field_values(self):
        comment_form = CommentForm()
        author = User.objects.create_user('test', '', 'test_passwd1')
        article = Article.objects.create()
        with self.assertRaises(ValidationError):
            comment_form.save(author, article)

    def test_comment_form_works_properly_with_correct_data(self):
        body = 'Test comment body'
        comment_form = CommentForm(data={'body': body})
        author = User.objects.create_user('test1', '', 'testtest_pass123')
        article = Article.objects.create()
        comment_form.save(author, article)
        self.assertIn(body, comment_form.cleaned_data.values())
        

class LoginFormTest(TestCase):

    def test_login_with_correct_user(self):
        user = User.objects.create_user('test_user', '', 'test_password3')
        request_data = {'password': 'test_password3',
                        'username': 'test_user'}
        request_querydict = QueryDict('', mutable=True)
        request_querydict.update(request_data)

        request = RequestFactory().post('/login', request_querydict)
        request.session = SessionStore()
        
        login_form = UserLoginForm(request, data=request.POST)
        self.assertTrue(login_form.is_valid())

    def test_attempt_login_with_incorrect_data(self):
        request_data = {'password': 'test',
                        'username': 'testtest'}
        request_querydict = QueryDict('', mutable=True)
        request_querydict.update(request_data)

        request = RequestFactory().post('/login', request_querydict)
        request.session = SessionStore()

        login_form = UserLoginForm(request, data=request.POST)
        self.assertFalse(login_form.is_valid())
        with self.assertRaises(ValidationError):
            login_form.login()


class UserSignupFormTest(TestCase):

    def test_signup_new_user_with_correct_data(self):
        new_user = {'username': 'new_username',
                    'password1': 'my_new_password1',
                    'password2': 'my_new_password1'}
        
        signup_form = UserSignupForm(data=new_user)
        new_user_obj = signup_form.save()
        self.assertEqual(new_user['username'], new_user_obj.username)

    def test_signup_new_user_with_incorrect_data(self):
        new_user = {'username': '',
                    'password1': '',
                    'password2': ''}
        signup_form = UserSignupForm(data=new_user)
        with self.assertRaises(ValueError):
            signup_form.save()

    def test_try_registering_user_with_existing_username(self):
        new_user = {'username': 'new_username',
                    'password1': 'my_new_password1',
                    'password2': 'my_new_password1'}

        User.objects.create_user(new_user['username'], '', new_user['password1'])
        signup_form = UserSignupForm(data=new_user)
        with self.assertRaises(ValueError):
            signup_form.save()

    def test_try_registering_user_with_incomplete_fields(self):
        new_user = {'username': 'new_username', 'password1': 'my_new_password1'}
        signup_form = UserSignupForm(data=new_user)
        with self.assertRaises(ValueError):
            signup_form.save()

