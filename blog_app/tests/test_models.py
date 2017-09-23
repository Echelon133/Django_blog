from django.test import TestCase
from blog_app.models import Category, Article, Comment, User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class CategoryModelTest(TestCase):

    def test_create_valid_category(self):
        name = 'my-category-name'
        category = Category(name=name)
        category.full_clean()
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
        category.full_clean()
        category.save()

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


class CommentModelTest(TestCase):
    
    @staticmethod
    def get_new_comment(*, author=None, article_commented=None, body=None):
        if author is None:
            author = ''
        else:
            author = author
        
        if article_commented is None:
            article_commented = ''
        else:
            article_commented = article_commented
        
        if body is None:
            body = ''
        else:
            body = body

        new_comment = Comment.objects.create(author=author, article_commented=article_commented, body=body)
        return new_comment
    
    def test_create_valid_comments(self):
        author1 = User.objects.create_user('test_user', '', 'test_password1')
        author2 = User.objects.create_user('test_user2', '', 'test_password123')
        article1 = Article.objects.create()

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
        author1 = User.objects.create_user('test_user', '', 'user_password_111')
        article1 = Article.objects.create()

        comment = self.get_new_comment(author=author1, article_commented=article1)
        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_try_creating_comment_without_author(self):
        article1 = Article.objects.create()

        with self.assertRaises(ValueError):
            comment = self.get_new_comment(article_commented=article1, body='Test')

    def test_try_creating_comment_without_article(self):
        author1 = User.objects.create_user('test_user', '', 'user_passwd123')

        with self.assertRaises(ValueError):
            comment = self.get_new_comment(author=author1, body='Test')