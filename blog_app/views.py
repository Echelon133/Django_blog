from django.views import View
from django.shortcuts import render
from django.contrib.auth.views import logout
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Article, Category, Comment, User
from .forms import UserSignupForm, UserLoginForm, CommentForm


class BaseView(TemplateView):
    login_form = UserLoginForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'login_form': self.login_form})
        return context
    
    def get_page_context(self, objects, page):
        paginator = Paginator(objects, 5)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return articles


class HomepageView(BaseView):
    template_name = "blog_app/homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        all_articles = Article.objects.all()[::-1]
        articles = self.get_page_context(all_articles, page)
        context['articles'] = articles
        return context


class CategoryView(BaseView):
    template_name = 'blog_app/category.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = context['category_name']
        try:
            category_obj = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            return context
        else:
            page = self.request.GET.get('page')
            filtered_articles = Article.objects.filter(category=category_obj)[::-1]
            articles = self.get_page_context(filtered_articles, page)
            context['articles'] = articles
            return context


class SearchByBaseView(BaseView):
    template_name = 'blog_app/by_date.html'


class SearchByYearView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = context['year']
        page = self.request.GET.get('page')
        filtered_articles = Article.objects.filter(last_modified__year=year)
        articles = self.get_page_context(filtered_articles, page)
        context.update(
            {'searched_date': "{year}".format(year=year),
             'articles': articles})
        return context


class SearchByMonthView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        year = context['year']
        month = context['month']
        page = self.request.GET.get('page')
        filtered_articles = Article.objects.filter(last_modified__year=year,
                                                   last_modified__month=month)
        articles = self.get_page_context(filtered_articles, page)
        context.update(
            {'searched_date': "{year}/{month}".format(year=year, month=month),
             'articles': articles})
        return context 


class SearchByDayView(SearchByBaseView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        year = context['year']
        month = context['month']
        day = context['day']
        page = self.request.GET.get('page')
        filtered_articles = Article.objects.filter(last_modified__year=year,
                                                   last_modified__month=month,
                                                   last_modified__day=day)
        articles = self.get_page_context(filtered_articles, page)
        context.update(
            {'searched_date': "{year}/{month}/{day}".format(year=year,
                                                            month=month,
                                                            day=day),
             'articles': articles})
        return context


class PageNotFoundView(BaseView):
    template_name = 'blog_app/404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleView(View):
    template_name = 'blog_app/article.html'
    login_form = UserLoginForm()
    comment_form = CommentForm()

    def get_article_comments(self, article_id):
        comments = Comment.objects.filter(article_commented__article_id=article_id)
        return comments

    def get(self, request, *args, **kwargs):
        article_id = kwargs['article_id']
        try:
            article_obj = Article.objects.get(article_id=article_id)
        except Article.DoesNotExist:
            raise 404

        comment_form = CommentForm()
        comments = self.get_article_comments(article_id)
        
        context = {'title': article_obj.title,
                   'last_modified': article_obj.last_modified,
                   'categories': article_obj.category.all(),
                   'article_body': article_obj.article_body,
                   'comments': comments,
                   'login_form': self.login_form,
                   'comment_form': self.comment_form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)

        author = request.user
        article = Article.objects.get(article_id=kwargs['article_id'])
        
        if comment_form.is_valid():
            comment_form.save(author, article)
        return HttpResponseRedirect(request.get_full_path())


class SignupView(View):
    template_name = 'blog_app/signup.html'

    def get(self, request, *args, **kwargs):
        form = UserSignupForm()
        arguments = {'form': form}
        arguments.update(csrf(request))
        return render(request, self.template_name, arguments)

    def post(self, request, *args, **kwargs):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, self.template_name)
        else:
            return render(request, self.template_name, {'user_exists': True,
                                                        'form': UserSignupForm()})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            form.login()
        return HttpResponseRedirect('/')


class LogoutView(View):
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect('/')