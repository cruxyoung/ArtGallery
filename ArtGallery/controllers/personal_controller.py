from django.shortcuts import render, redirect
from.. import models
from django.http import HttpResponse


def personal_art_world(request, user_id):
    customer = models.User.objects.get(pk=user_id)
    favourites = models.FavoriteRecord.objects.filter(customer_id=user_id)
    fav_artworks = []
    for fav in favourites:
        fav_artworks.append(models.ArtWork.objects.get(pk=fav.id))
    return render(request, 'personal_center/personal_world.html',
                  {'customer': customer, 'fav_artworks': fav_artworks})
