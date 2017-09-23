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
        if sort == "time":
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
        if sort == 'price':
            auctions = auctions.order_by('-ah_amount')

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
    # get rewards history of current user
    rewards = models.Reward.objects.filter(customer_id=request.user.id)
    rewards_nums = rewards.count()

    # get sort info
    sort = request.GET.get('sort', "")
    if sort:
        if sort == 'time':
            rewards = rewards.order_by('-reward_time')
        if sort == 'price':
            rewards = rewards.order_by('-reward_amount')

    # Paginator for rewards
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(rewards, 6, request=request)
    rewards_pag = p.page(page)

    return render(request,
                  'personal_center/personal_center_rewards.html',
                  {'customer': request.user,
                   'rewards': rewards_pag,
                   'rewards_nums': rewards_nums,
                   'sort': sort,
                   })


def personal_comments_default(request):
    # get comments history of current user
    comments = models.Comment.objects.filter(commenter_id=request.user.id)
    comments_nums = comments.count()

    # get sort info
    sort = request.GET.get('sort', "")
    if sort:
        if sort == 'time':
            comments = comments.order_by('-comment_time')
        if sort == 'comment':
            comments = comments.filter(replay_commentId=0)
        if sort == 'reply':
            comments = comments.filter(rating=-1)

    # Paginator for rewards
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(comments, 3, request=request)
    comments_pag = p.page(page)

    return render(request,
                  'personal_center/personal_center_comments.html',
                  {'customer': request.user,
                   'comments': comments_pag,
                   'comments_nums': comments_nums,
                   'sort': sort,
                   })


def personal_settings_default(request):
    # get personal detail of current user
    return render(request,
                  'personal_center/personal_center_settings.html',
                  {'customer': request.user})


def personal_complaints_default(request):
    # get complaints history of current user
    complaints = models.Complaint.objects.filter(customer_id=request.user.id)
    complaints_nums = complaints.count()

    # Paginator for rewards
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(complaints, 4, request=request)
    comments_pag = p.page(page)

    return render(request,
                  'personal_center/personal_center_complaints.html',
                  {'customer': request.user,
                   'complaints': comments_pag,
                   'complaints_nums': complaints_nums,
                   })
