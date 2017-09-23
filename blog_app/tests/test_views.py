from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve

from ..views import (HomepageView, CategoryView, 
                     SearchByYearView, SearchByMonthView, 
                     SearchByDayView, PageNotFoundView, 
                     ArticleView, SignupView, LoginView, 
                     LogoutView)
from ..forms import (UserSignupForm, UserCreationForm, 
                     CommentForm, UserLoginForm)
from ..models import Category, Article, User, Comment


class HomepageTest(TestCase):

    def test_home_page_renders_correct_template(self):
        res = self.client.get('/')
        self.assertTemplateUsed(res, 'blog_app/homepage.html')

    def test_home_page_has_correct_form_loaded(self):
        res = self.client.get('/')
        login_form = res.context['login_form']
        self.assertIsInstance(login_form, UserLoginForm)

    def test_home_page_loads_correct_articles(self):
        article1 = Article.objects.create(title='Test1')
        article2 = Article.objects.create(title='Test2')

        res = self.client.get('/')
        loaded_articles = res.context['articles']

        self.assertIn(article1, loaded_articles)
        self.assertIn(article2, loaded_articles)