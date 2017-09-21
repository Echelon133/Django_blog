from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore
from django.test.client import RequestFactory
from django import forms
from django.http import QueryDict
from blog_app.forms import UserLoginForm, UserSignupForm, CommentForm
from blog_app.models import User, Comment, Article


class CommentFormTest(TestCase):
    
    def test_comment_form_has_correct_restrictions(self):
        comment_form = CommentForm()
        self.assertIn('maxlength="500"', comment_form.as_p())
        self.assertIn('required', comment_form.as_p())

    def test_comment_form_fails_with_incorrect_field_values(self):
        comment_form = CommentForm()
        author = User.objects.create_user('test', '', 'test_passwd1')
        article = Article.objects.create()
        with self.assertRaises(forms.ValidationError):
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