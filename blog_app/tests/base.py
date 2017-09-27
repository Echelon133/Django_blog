from django.test import TestCase
from blog_app.models import Category, Article, Comment, User
from django.utils.text import slugify


class CustomTestCase(TestCase):
    
    def get_new_category(self, *, name=None):
        new_category = Category.objects.create(name=name)
        return new_category

    def get_new_article(self, *, title=None, category=None, article_body=None):
        if title is None:
            title = ''
            slug = ''
        else:
            title = title
            slug = slugify(title)
        
        if category is None:
            category = []
        else:
            category = category

        if article_body is None:
            article_body = ''
        else:
            article_body = article_body

        new_article = Article.objects.create()
        new_article.title = title
        new_article.category = category
        new_article.article_body = article_body
        new_article.slug = slug
        return new_article

    def get_new_user(self, *, username, password):
        new_user = User.objects.create_user(username, '', password)
        return new_user

    def get_new_comment(self, *, author=None, article_commented=None, body=None):
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
        
