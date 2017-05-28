import uuid
from django.db import models

def generate_id():
    uid = uuid.uuid4().hex
    return uid[:6]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=40)


class Article(models.Model):
    article_id = models.CharField(primary_key=True, 
                                  default=generate_id,
                                  editable=False,
                                  max_length=6)
    title = models.CharField(max_length=100)
    last_modified = models.DateField(auto_now=True)
    author = models.CharField(default='Admin',
                              max_length=30)
    category = models.ManyToManyField(Category)
    article_body = models.TextField()
    slug = models.SlugField()