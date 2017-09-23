import json
from django.http import HttpResponse
from django.shortcuts import render
from .. import models
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


def personal_favorite_default(request):
    # get favorites of current user
    favs = models.FavoriteRecord.objects.filter(customer_id=request.user.id)
    favs_nums = favs.count()

    # get sort info
    sort = request.GET.get('sort', "")
    if sort:
        if sort == "like_time":
            favs = favs.order_by('fav_time')

    # Paginator for favorite
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(favs, 6, request=request)
    favs_pag = p.page(page)
    return render(request,
                  'personal_center/personal_center_favorites.html',
                  {'customer': request.user,
                   'favs': favs_pag,
                   'favs_nums': favs_nums,
                   'sort': sort,
                   })


def personal_auctions_default(request):
    # get auctions history of current user
    auctions = models.AuctionHistory.objects.filter(customer_id=request.user.id)
    auctions_nums = auctions.count()

    # get sort info
    sort = request.GET.get('sort', "")
    if sort:
        if sort == "time":
            auctions = auctions.order_by('-ah_aucTime')
        # sort == 'price'
        else:
            auctions = auctions.order_by('ah_amount')

    # Paginator for auctions
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(auctions, 4, request=request)
    auctions_pag = p.page(page)
    return render(request,
                  'personal_center/personal_center_auctions.html',
                  {'customer': request.user,
                   'auctions': auctions_pag,
                   'auctions_nums': auctions_nums,
                   'sort': sort,
                   })


def personal_rewards_default(request):
    rewards = models.Reward.objects.filter(customer_id=request.user.id)
    return render(request,
                  'personal_center/personal_center_rewards.html',
                  {'rewards': rewards,
                   'customer': request.user},
                  )


def personal_comments_default(request):
    comments = models.Comment.objects.filter(commenter_id=request.user.id)
    return render(request,
                  'personal_center/personal_center_comments.html',
                  {'comments': comments,
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
