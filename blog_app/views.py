from django.shortcuts import render
from django.http import Http404
from django.views.generic import TemplateView


from .models import Article
from .models import Category
from .models import SiteDetails


class BaseView(TemplateView):
    site_details = SiteDetails.objects.get(pk=1)
    # Dict with site info that every other view inherits
    baseview_context = {'headline':site_details.headline,
                        'description':site_details.description,
                        'author_nick':site_details.author_nick,
                        'author_description':site_details.author_description,
                        'authors_twitter':site_details.authors_twitter,
                        'authors_facebook':site_details.authors_facebook,
                        'authors_github':site_details.authors_github,
                        'authors_youtube':site_details.authors_youtube}


class HomepageView(BaseView):
    template_name = "blog_app/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        articles = Article.objects.all()
        context['articles'] = articles
        return context


class ArticleView(BaseView):
    template_name = 'blog_app/article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        article_id = context['article_id']
        try:
            article_obj = Article.objects.get(article_id=article_id)
        except Article.DoesNotExist:
            raise Http404
        context['title'] = article_obj.title
        context['last_modified'] = article_obj.last_modified
        context['categories'] = article_obj.category.all()
        context['article_body'] = article_obj.article_body
        return context


class CategoryView(BaseView):
    template_name = 'blog_app/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        category_name = context['category_name']
        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            # return context without 'articles' var, so appropriate message can be displayed
            return context
        else:
            context['articles'] = Article.objects.filter(category=category_obj)
        return context


class SearchByBaseView(BaseView):
    template_name = 'blog_app/by_date.html'


class SearchByYearView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        year = context['year']
        context['searched_date'] = "{year}".format(year=year)
        context['articles'] = Article.objects.filter(last_modified__year=year)
        return context


class SearchByMonthView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        year = context['year']
        month = context['month']

        context['searched_date'] = "{year}/{month}".format(year=year, month=month)
        context['articles'] = Article.objects.filter(last_modified__year=year,
                                                     last_modified__month =month)
        return context 


class SearchByDayView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.baseview_context)
        
        year = context['year']
        month = context['month']
        day = context['day']

        context['searched_date'] = "{year}/{month}/{day}".format(year=year,
                                                                 month=month,
                                                                 day=day)
        context['articles'] = Article.objects.filter(last_modified__year=year,
                                                     last_modified__month=month,
                                                     last_modified__day=day)
        return context


class PageNotFoundView(BaseView):
    template_name = 'blog_app/404.html'
