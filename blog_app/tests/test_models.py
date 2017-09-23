from django.test import TestCase
from blog_app.models import Category, Article, Comment
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CategoryModelTest(TestCase):

    def test_create_valid_category(self):
        name = 'my-category-name'
        category = Category(name=name)
        category.save()

        self.assertEqual(name, str(category))
        url = '/category/' + name
        self.assertEqual(url, category.get_absolute_url())

    def test_try_creating_category_with_invalid_characters(self):
        name = 'name!\n%^&(*#@#$)'
        expected_name = 'name'
        category = Category(name=name)
        # When saving, category name is cleared from
        # invalid characters. Only alphanum characters
        # and - + are allowed
        category.save()
        category.full_clean()

        self.assertEqual(str(category), expected_name)

    def test_try_creating_empty_category(self):
        category = Category()
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_try_creating_category_with_long_name(self):
        name = 'Test' * 100
        category = Category(name=name)
        with self.assertRaises(ValidationError):
            category.full_clean()


class ArticleModelTest(TestCase):
    
    @staticmethod
    def get_new_article(*, title=None, category=None, article_body=None):
        if title is None:
            art_title = ''
            art_slug = ''
        else:
            art_title = title
            art_slug = slugify(title)
        
        if category is None:
            art_category = []
        else:
            art_category = category

        if article_body is None:
            art_body = ''
        else:
            art_body = article_body

        new_article = Article.objects.create()
        new_article.title = art_title
        new_article.category = art_category
        new_article.article_body = art_body
        new_article.slug = art_slug
        return new_article
    
    def test_create_valid_article(self):
        category1 = Category.objects.create(name='test-category')
        test_article = {'title': 'My article title',
                        'category': [category1, ],
                        'article_body': 'text' * 200}
        
        article = self.get_new_article(title=test_article['title'],
                                       category=test_article['category'],
                                       article_body=test_article['article_body'])
        article.full_clean()

        self.assertEqual(article.title, test_article['title'])
        self.assertEqual(article.category.first(), test_article['category'][0])
        self.assertEqual(article.article_body, test_article['article_body'])
        self.assertEqual(article.slug, slugify(test_article['title']))
        self.assertEqual(article.title, str(article))

        url = "/{hash}/{slug}".format(hash=article.article_id, slug=article.slug)
        self.assertEqual(url, article.get_absolute_url())

    def test_try_creating_article_without_title(self):
        category1 = Category.objects.create(name='test-category')
        test_article = {'title': '',
                        'category': [category1, ],
                        'article_body': 'text' * 200}

        article = self.get_new_article(title=test_article['title'],
                                       category=test_article['category'],
                                       article_body=test_article['article_body'])
        
        with self.assertRaises(ValidationError):
            article.full_clean()

    def test_try_creating_article_without_body(self):
        category1 = Category.objects.create(name='test-category')
        test_article = {'title': 'My article title',
                        'category': [category1, ],
                        'article_body': ''}

        article = self.get_new_article(title=test_article['title'],
                                       category=test_article['category'],
                                       article_body=test_article['article_body'])
        
        with self.assertRaises(ValidationError):
            article.full_clean()

