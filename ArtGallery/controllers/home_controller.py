from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from ArtGallery.models import ArtWork
from django import forms
from ..forms import SearchForm


def home_page(request):
    artworks = ArtWork.objects.all()
    if len(artworks)>=6:
        latest_artworks = artworks.order_by('aw_time')[len(artworks)-6  :]
    else:
        latest_artworks = None
    print(artworks[2].aw_img)
    return render(request,
                  'home_page/index.html',
                  {'artworks': artworks,
                   'latest_artworks':latest_artworks,
                   'example0':artworks[0],
                   'example1': artworks[1],
                   'example2': artworks[2],
                   'example3': artworks[3],
                   'example4': artworks[4],

                   })


def detail(request, art_id):
    return HttpResponse("You're looking at question %s." % art_id)


# art_list page
def art_list(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():

            return HttpResponse('fifdsafidsaf')

    return render(request, 'home_page/art_list.html')

# def get_filter(request):
#     if request.method == 'POST':
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             return HttpResponse('form success')
#         else:
#
#             return HttpResponse('form fail')

