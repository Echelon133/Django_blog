from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def homepage(request):
    return HttpResponse("homepage")

def article(request, article_id):
    return HttpResponse("article id: {}".format(article_id))

def category(request, category_name):
    return HttpResponse("category: {}".format(category_name))

def by_year(request, year):
    return HttpResponse("by_year: {}".format(year))

def by_month(request, year, month):
    return HttpResponse("by_month: {}/{}".format(year, month))

def by_day(request, year, month, day):
    return HttpResponse("by_day: {}/{}/{}".format(year, month, day))
