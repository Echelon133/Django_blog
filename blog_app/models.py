import uuid
import re
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


def generate_id():
    uid = uuid.uuid4().hex
    return uid[:6]


def remove_not_safe(text):
    expr = re.compile('[^a-zA-Z0-9 +\-]')
    text = expr.sub('', text)
    return text


class Category(models.Model):
    name = models.CharField(max_length=20, blank=False)

    def save(self, *args, **kwargs):
        self.name = remove_not_safe(self.name.lower())
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=[self.name])


class Article(models.Model):
    article_id = models.CharField(primary_key=True, 
                                  default=generate_id,
                                  editable=False,
                                  max_length=6,
                                  unique=True)
    title = models.CharField(max_length=100, blank=False, null=False)
    last_modified = models.DateField(auto_now=True)
    category = models.ManyToManyField(Category)
    article_body = models.TextField(blank=False)
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', args=[self.article_id, self.slug])


class Comment(models.Model):
    author = models.ForeignKey(User, null=False)
    article_commented = models.ForeignKey(Article, null=False)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.author, self.body[:20])
