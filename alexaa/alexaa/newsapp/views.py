# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from newsapp.forms import *
from newsapp.models import *

# Create your views here.

def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    if request.method == "POST":
        if form.is_valid():
            fname = form.cleaned_data['f_name']
            lname = form.cleaned_data['l_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            print User.objects.filter(username=email).exists()
            if User.objects.filter(username=email).exists():
                print "User Exists"
            else:
                user = User.objects.create_user(username=email, email=email, password=password,
                                                last_name=lname, first_name=fname)
                profile = Profile.objects.create(phone_number=phone, user=user)
                profile.save()
                user.save()
                return HttpResponse("<h3>Success</h3>")
    return render(request, 'forms/signup.html', locals())

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                redirect("login")

    return render(request, 'forms/login.html', locals())

def logout_view(request):
    logout(request)
    return redirect("home")

def home(request):
    articles = NewsArticle.objects.all()
    categories = Category.objects.all()
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    return render(request, 'home.html', locals())

def articles_view(request, category, slug):
    form = CommentForm(request.POST or None)
    categories = Category.objects.all()
    article = get_object_or_404(NewsArticle, slug=slug)
    comments = Comment.objects.filter(article=article)
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    if request.is_ajax():
        type_of = request.POST['parameter']; get_data = request.POST['data']
        if type_of == u"like":
            likes = NewsArticle.objects.get(slug=slug)
            likes.like = likes.like + 1
            likes.save()
            return JsonResponse({'success':'like'})
        elif type_of == u"dislike":
            dislikes = NewsArticle.objects.get(slug=slug)
            dislikes.dislike = dislikes.dislike + 1
            dislikes.save()
            return JsonResponse({'success': 'dislike'})
        elif type_of == u"delete":
            print "delete"
            print get_data
            comment = Comment.objects.filter(article=article, body=get_data, user=request.user)
            comment.delete()
            return JsonResponse({'success':'delete'})
    if request.method == "POST":
        get_data = request.POST['data']
        comment = Comment.objects.create(article=article, body=get_data, user=request.user)
        comment.save()
        return articles_view(request, category, slug)
    return render(request, "article.html", locals())

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    details = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=details)
    form = ProfileForm(request.POST or None,
                       initial={'f_name':details.first_name,'l_name':details.last_name,'phone':profile.phone_number})
    if request.method == "POST":
        if form.is_valid():
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            phone = form.cleaned_data['phone']
            details.first_name = f_name; details.last_name =l_name; profile.phone_number = phone
            details.save()
            profile.save()
            return HttpResponse("Done")
    return render(request, "edit-profile.html", locals())

def category_view(request, category):
    category = Category.objects.get(category=category)
    categories = Category.objects.all()
    articles = NewsArticle.objects.filter(category=category)
    if request.method == 'GET':
        try:
            obj = request.GET['search-value']
            search = NewsArticle.objects.filter(Q(body__icontains=obj) | Q(header__icontains=obj)).distinct()
            return render(request, 'search.html', locals())
        except:
            pass
    return render(request, "category-list.html", locals())

