from django.test import TestCase
from django import forms
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
        