# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from froala_editor.fields import FroalaField

from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """
        Profile models
        User phone number linked with the user
    """
    phone_number = models.IntegerField()
    user = models.ForeignKey(User)

    # Admin display
    def __str__(self):
        return self.user

class Category(models.Model):
    """
        Sections for news articles
    """
    category = models.CharField(max_length=25, unique=True)
    slug = models.SlugField(max_length=50)

    # get_absolute_url, to attach a url link with each row of this table
    @models.permalink
    def get_absolute_url(self):
        return ("category-list", [self.category.lower()])

    # Admin display
    def __str__(self):
        return self.category

    class Meta:
        """
            Helps in what to display in the admin in plural word
        """
        verbose_name_plural = "categories"

class NewsArticle(models.Model):
    """
        News article model
    """
    header = models.CharField(max_length=30)
    author = models.CharField(max_length=25)
    body = FroalaField(max_length=5000)
    time_stamp = models.DateTimeField(auto_created=True, auto_now_add=True)
    category = models.ForeignKey(Category)
    slug = models.SlugField(unique=True, blank=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

    # get_absolute_url, to attach a url link with each row of this table
    @models.permalink
    def get_absolute_url(self):
        return ("article", [self.category,self.slug])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        date = datetime.today()
        self.slug = "%i-%i-%i-%s" % (date.year, date.month, date.day, slugify(self.header))
        super(NewsArticle, self).save()

class Comment(models.Model):
    """
        Comments models
    """
    article = models.ForeignKey(NewsArticle)
    user = models.ForeignKey(User)
    body = models.TextField(max_length=5000)
    time_stamp = models.DateTimeField(auto_created=True, auto_now_add=True)

    # Admin display
    def __str__(self):
        return self.user