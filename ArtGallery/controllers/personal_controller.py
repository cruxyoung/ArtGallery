import json
from django.http import HttpResponse
from django.shortcuts import render
from.. import models
from django.http import JsonResponse


def personal_favorite_default(request):
    favourites = models.FavoriteRecord.objects.filter(customer_id=request.user.id)
    fav_artworks = []
    for fav in favourites:
        fav_artworks.append(models.ArtWork.objects.get(pk=fav.id))
    return render(request,
                  'personal_center/personal_center_favorites.html',
                  {'fav_artworks': fav_artworks,
                   'customer': request.user},
                  )


def personal_settings_default(request):
    return render(request,
                  'personal_center/personal_center_settings.html',
                  {'customer': request.user},
                  )


def personal_complaints_default(request):
    complaints = models.Complaint.objects.filter(customer_id=request.user.id)
    return render(request,
                  'personal_center/personal_center_complaints.html',
                  {'complaints': complaints,
                   'customer': request.user},
                  )


def personal_rewards_default(request):
    rewards = models.Reward.objects.filter(customer_id=request.user.id)
    return render(request,
                  'personal_center/personal_center_rewards.html',
                  {'rewards': rewards,
                   'customer': request.user},
                  )
