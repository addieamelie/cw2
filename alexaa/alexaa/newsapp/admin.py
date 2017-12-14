# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from newsapp.models import *

# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    """
        Defining how models are structured in the admin page
    """
    list_display = ['time_stamp', 'body', 'author'] # What to display in the admin page of newarticle
    search_fields = ['body'] # Where to search to make queries in the admin page of newsarticle
    list_filter = ['category'] # Filtering result to be displayed in the newarticle page

class CategoryAdmin(admin.ModelAdmin):
    """
        Defining how models are structured in the admin page
    """
    list_display = ['category'] # What to display in the admin page of newarticle
    prepopulated_fields = {'slug':('category',),} # Prepopulating the slug field automatically


# Registering the models with the admin for display
admin.site.register(NewsArticle, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
