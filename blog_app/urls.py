from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/?$', views.SearchByDayView.as_view(), name='by_day'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/?$', views.SearchByMonthView.as_view(), name='by_month'),
    url(r'^(?P<year>[0-9]{4})/?$', views.SearchByYearView.as_view(), name='by_year'),
    url(r'^category/(?P<category_name>[A-Za-z_ \-0-9+]+)', views.CategoryView.as_view(), name='category'),
    url(r'^(?P<article_id>[A-Za-z0-9]{6})/(?P<slug>[a-zA-z\-]+)', views.ArticleView.as_view(), name='article'),
    url(r'^signup', views.SignupView.as_view(), name='signup'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
]