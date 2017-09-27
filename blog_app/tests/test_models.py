from blog_app.models import Category, Article, Comment, User
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .base import CustomTestCase


class CategoryModelTest(CustomTestCase):

    def test_create_valid_category(self):
        name = 'my-category-name'
        category = self.get_new_category(name=name)
        category.full_clean()
        category.save()

        self.assertEqual(name, str(category))
        url = '/category/' + name
        self.assertEqual(url, category.get_absolute_url())

    def test_try_creating_category_with_invalid_characters(self):
        name = 'name!\n%^&(*#@#$)'
        expected_name = 'name'
        category = self.get_new_category(name=name)
        # When saving, category name is cleared from
        # invalid characters. Only alphanum characters
        # and - + are allowed
        category.full_clean()
        category.save()

        self.assertEqual(str(category), expected_name)

    def test_try_creating_empty_category(self):
        category = self.get_new_category(name='')
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_try_creating_category_with_long_name(self):
        name = 'Test' * 100
        category = self.get_new_category(name=name)
        with self.assertRaises(ValidationError):
            category.full_clean()


class ArticleModelTest(CustomTestCase):
    
    def test_create_valid_article(self):
        category1 = self.get_new_category(name='test-category')
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
        category1 = self.get_new_category(name='test-category')
        test_article = {'title': '',
                        'category': [category1, ],
                        'article_body': 'text' * 200}

        article = self.get_new_article(title=test_article['title'],
                                       category=test_article['category'],
                                       article_body=test_article['article_body'])
        
        with self.assertRaises(ValidationError):
            article.full_clean()

    def test_try_creating_article_without_body(self):
        category1 = self.get_new_category(name='test-category')
        test_article = {'title': 'My article title',
                        'category': [category1, ],
                        'article_body': ''}

        article = self.get_new_article(title=test_article['title'],
                                       category=test_article['category'],
                                       article_body=test_article['article_body'])
        
        with self.assertRaises(ValidationError):
            article.full_clean()


class CommentModelTest(CustomTestCase):
    
    def test_create_valid_comments(self):
        author1 = self.get_new_user(username='test_user', password='test_password1')
        author2 = self.get_new_user(username='test_user2', password='test_password123')
        article1 = self.get_new_article()

        comment1 = self.get_new_comment(author=author1, article_commented=article1, body='Test')
        comment2 = self.get_new_comment(author=author2, article_commented=article1, body='Another text')

        comment1.full_clean()
        comment2.full_clean()

        self.assertEqual(comment1.author, author1)
        self.assertEqual(comment1.article_commented, article1)
        self.assertEqual(comment1.body, 'Test')
        self.assertEqual(comment2.author, author2)
        self.assertEqual(comment2.article_commented, article1)
        self.assertEqual(comment2.body, 'Another text')

        str_ = '{} - {}'
        self.assertEqual(str(comment1), str_.format(comment1.author, comment1.body[:20]))
        self.assertEqual(str(comment2), str_.format(comment2.author, comment2.body[:20]))

    def test_try_creating_comment_without_body(self):
        author1 = self.get_new_user(username='test_user', password='user_password_111')
        article1 = self.get_new_article()

        comment = self.get_new_comment(author=author1, article_commented=article1)
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_try_creating_comment_without_author(self):
        article1 = self.get_new_article()

        with self.assertRaises(ValueError):
            comment = self.get_new_comment(article_commented=article1, body='Test')

    def test_try_creating_comment_without_article(self):
        author1 = self.get_new_user(username='test_user', password='user_passwd123')

        with self.assertRaises(ValueError):
            comment = self.get_new_comment(author=author1, body='Test')