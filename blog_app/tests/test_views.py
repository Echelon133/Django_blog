from django.test import TestCase
from django.http import HttpRequest
from django.core.urlresolvers import resolve
from datetime import datetime

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

    
class SearchByDateTest(TestCase):
    date_now = datetime.now()
    current_year = str(date_now.year)
    current_month = str(date_now.month).zfill(2)
    current_day = str(date_now.day).zfill(2)
    
    def setUp(self):
        self.res1 = None
        self.res2 = None
        self.res3 = None

        self.category = Category.objects.create()
        self.category.name = 'category'
        self.category.save()

        self.article = Article.objects.create()
        self.article.title = 'Test article'
        self.article.category = [self.category, ]
        self.article.body = 'Test'
        self.article.slug = 'test-article'
        self.article.save()
        
    def update_responses(self):
        self.res1 = self.client.get('/{}'.format(self.current_year))
        self.res2 = self.client.get('/{}/{}'.format(self.current_year, 
                                                    self.current_month))
        self.res3 = self.client.get('/{}/{}/{}'.format(self.current_year,
                                                       self.current_month,
                                                       self.current_day))

    def test_search_date_pages_render_correct_templates(self):
        self.update_responses()
        self.assertTemplateUsed(self.res1, 'blog_app/by_date.html')
        self.assertTemplateUsed(self.res2, 'blog_app/by_date.html')
        self.assertTemplateUsed(self.res3, 'blog_app/by_date.html')

    def test_search_date_page_has_correct_form_loaded(self):
        self.update_responses()

        login_form1 = self.res1.context['login_form']
        login_form2 = self.res2.context['login_form']
        login_form3 = self.res3.context['login_form']

        self.assertIsInstance(login_form1, UserLoginForm)
        self.assertIsInstance(login_form2, UserLoginForm)
        self.assertIsInstance(login_form3, UserLoginForm)

    def test_search_date_pages_have_correct_form_loaded(self):
        self.update_responses()
        login_form1 = self.res1.context['login_form']
        login_form2 = self.res2.context['login_form']
        login_form3 = self.res3.context['login_form']
        
        self.assertIsInstance(login_form1, UserLoginForm)
        self.assertIsInstance(login_form2, UserLoginForm)
        self.assertIsInstance(login_form3, UserLoginForm)
    
    def test_search_date_pages_load_correct_articles(self):
        # Get page after adding new article to the database
        self.update_responses()

        self.assertIn(self.article, self.res1.context['articles'])
        self.assertIn(self.article, self.res2.context['articles'])
        self.assertIn(self.article, self.res3.context['articles'])
    
    def test_search_date_page_displays_correct_info_texts(self):
        self.update_responses()
        self.assertContains(self.res1, 'Searching by date: {}'.format(self.current_year))
        self.assertContains(self.res2, 'Searching by date: {}/{}'.format(self.current_year, 
                                                                         self.current_month))
        self.assertContains(self.res3, 'Searching by date: {}/{}/{}'.format(self.current_year, 
                                                                            self.current_month, 
                                                                            self.current_day))


class PageNotFoundTest(TestCase):
    
    def test_404_page_renders_correct_template(self):
        # Article that does not exist
        res = self.client.get('/aaaaaa')
        self.assertTemplateUsed(res, 'blog_app/404.html')


class ArticleTest(TestCase):
    base_url = '/{hash_}/{slug}'
    
    def setUp(self):
        self.category = Category.objects.create()
        self.category.name = 'category'
        self.category.save()
        
        self.article = Article.objects.create()
        self.article.title = 'Test article'
        self.article.category = [self.category, ]
        self.article.body = 'Test'
        self.article.slug = 'test-article'
        self.article.save()

        self.user = User.objects.create_user('test_user1', '', 'test_password123')
        self.user.save()
        
        self.comment = Comment.objects.create(author=self.user,
                                              article_commented=self.article,
                                              body='test')
        self.comment.save()
    
    def test_article_page_renders_correct_template(self):
        res = self.client.get(self.base_url.format(hash_=self.article.article_id, 
                                                   slug=self.article.slug))
        self.assertTemplateUsed(res, 'blog_app/article.html')

    def test_article_page_has_correct_forms_loaded(self):
        res = self.client.get(self.base_url.format(hash_=self.article.article_id, 
                                                   slug=self.article.slug))
        login_form = res.context['login_form']
        comment_form = res.context['comment_form']
        self.assertIsInstance(login_form, UserLoginForm)
        self.assertIsInstance(comment_form, CommentForm)

    def test_article_page_displays_correct_article(self):
        res = self.client.get(self.base_url.format(hash_=self.article.article_id,
                                                   slug=self.article.slug))
        self.assertEqual(res.context['title'], self.article.title)
        self.assertEqual(res.context['article_body'], self.article.article_body)

    def test_article_page_loads_comment(self):
        res = self.client.get(self.base_url.format(hash_=self.article.article_id,
                                                   slug=self.article.slug))
        self.assertIn(self.comment, res.context['comments'])






        

