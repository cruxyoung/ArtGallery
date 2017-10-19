from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from ArtGallery.models import ArtWork
from django import forms
from ..forms import SearchForm
import json



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
    # print(request.is_ajax())


    if request.method == "POST" and request.is_ajax():
        # print('success')
        form = SearchForm(request.POST)
        # print(form)
        if form.is_valid():
            filt = request.POST.get('filter','')
            # print(request.POST.getlist('f'))
            print(request.POST.getlist('genre-form'))
            print(request.POST.getlist('period-form'))

            artworks = ArtWork.objects.filter(aw_name__contains=filt)
            if request.POST.getlist("genre-form"):
                genre = request.POST.getlist("genre-form")[0]
                artworks = artworks.filter(aw_genre=genre)
            if request.POST.getlist('period-form'):
                period = request.POST.getlist('period-form')[0]
                artworks = artworks.filter(aw_time__year=period)

            artworks = list(artworks.values('aw_name','aw_genre'))

            return HttpResponse(json.dumps(artworks), content_type='application/json')



    return render(request, 'home_page/art_list.html')
