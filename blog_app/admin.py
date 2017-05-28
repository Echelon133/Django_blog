from django.contrib import admin
from .models import Category, Article, SiteDetails
# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug":("title",)}

admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(SiteDetails)