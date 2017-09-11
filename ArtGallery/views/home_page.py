from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from ..models import ArtWork
from django import forms
def home_page(request):


    artworks = ArtWork.objects.all()
    return render(request, 'home_page/home_page.html', {'artworks':artworks})

def detail(request, art_id):
    return HttpResponse("You're looking at question %s." % art_id)

# art_list page
def art_list(request):
    if request.method == "GET":

        keyword = request.GET['keyword']
        print(keyword)
        return HttpResponse('post')
    return HttpResponse("hello,this is the list")
