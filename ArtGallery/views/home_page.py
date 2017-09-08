from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from ..models import ArtWork

def home_page(request):
    artworks = ArtWork.objects.all()
    for a in artworks:
        print(a.aw_name)
    return render(request, 'home_page/home_page.html', {'artworks':artworks})