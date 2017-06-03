import uuid
import re
from django.db import models

def generate_id():
    uid = uuid.uuid4().hex
    return uid[:6]

def remove_not_safe(text):
    expr = re.compile('[^a-zA-Z0-9 +\-]')
    text = expr.sub('', text)
    return text


class SiteDetails(models.Model):
    headline = models.CharField(max_length=70)
    description = models.TextField(max_length=120)
    author_nick = models.CharField(max_length=100)
    author_description = models.TextField(max_length=300)
    authors_twitter = models.URLField(blank=True)
    authors_facebook = models.URLField(blank=True)
    authors_github = models.URLField(blank=True)
    authors_youtube = models.URLField(blank=True)


class Category(models.Model):
    name = models.CharField(max_length=40)

    def save(self, *args, **kwargs):
        self.name = remove_not_safe(self.name.lower())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    article_id = models.CharField(primary_key=True, 
                                  default=generate_id,
                                  editable=False,
                                  max_length=6)
    title = models.CharField(max_length=100)
    last_modified = models.DateField(auto_now=True)
    category = models.ManyToManyField(Category)
    article_body = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.title