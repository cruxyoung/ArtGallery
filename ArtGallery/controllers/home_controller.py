from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from ArtGallery.models import ArtWork
from django import forms


def home_page(request):
    artworks = ArtWork.objects.all()
    return render(request, 'home_page/home_page.html')
    # if len(artworks) < 0:
    #     return render(request, 'home_page/home_page.html')
    # else:
    #     latest_artworks = artworks.order_by('-aw_time')[:6]
    # # popular_artists = ArtWork.objects.all().order_by()
    # return render(request,
    #               'home_page/home_page.html',
    #               {'artworks': artworks,
    #                # 'popular_artists':
    #                'latest_artworks': latest_artworks,
    #                'example0': artworks[0],
    #                'example1': artworks[1],
    #                'example2': artworks[2],
    #                })


def detail(request, art_id):
    return HttpResponse("You're looking at question %s." % art_id)


# art_list page
def art_list(request):
    if request.method == "POST":
        keyword = request.POST['keyword']
        print(keyword)



    return render(request, 'home_page/art_list.html')
