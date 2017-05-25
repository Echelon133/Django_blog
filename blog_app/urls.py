from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})', views.by_day),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})', views.by_month),
    url(r'^(?P<year>[0-9]{4})', views.by_year),
    url(r'^category/(?P<category_name>[A-Za-z_\-0-9]+)', views.category),
    url(r'^(?P<article_id>[A-Za-z0-9]{6})', views.article),
    url(r'^', views.homepage, name='homepage'),

]