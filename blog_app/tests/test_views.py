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


class CategoryTest(TestCase):
    base_url = '/category/'

    def test_category_page_renders_correct_template(self):
        res = self.client.get(self.base_url + 'test')
        self.assertTemplateUsed(res, 'blog_app/category.html')

    def test_category_page_has_correct_form_loaded(self):
        res = self.client.get(self.base_url + 'test')
        login_form = res.context['login_form']
        self.assertIsInstance(login_form, UserLoginForm)

    def test_category_page_loads_correct_articles(self):
        category1 = Category.objects.create()
        category1.name = 'test-category'
        category1.save()

        categories = [category1, ]
        article1 = Article.objects.create()
        article1.title = 'Test article'
        article1.category = [category1, ]
        article1.save()

        res = self.client.get(self.base_url + category1.name)
        self.assertIn(article1, res.context['articles'])

    def test_category_page_doesnt_load_incorrect_articles(self):
        category1 = Category.objects.create()
        category1.name = 'category1'
        category1.save()
        
        category2 = Category.objects.create()
        category2.name = 'category2'
        category2.save()

        article1 = Article.objects.create()
        article1.title = 'Test'
        article1.category = [category1, ]
        article1.save()
        
        article2 = Article.objects.create()
        article2.title = 'Test2'
        article2.category = [category2, ]
        article2.save()

        res = self.client.get(self.base_url + category1.name)
        self.assertNotIn(article2, res.context['articles'])