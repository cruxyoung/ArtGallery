import json
from django.http import HttpResponse
from django.core import serializers
from _datetime import datetime
from ArtGallery.forms import CommentForm, RewardForm, AuctionCreateForm
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from ArtGallery.models import ArtWork, UserProfile, AuctionHistory, AuctionRecord, Comment, Reward, FavoriteRecord
from django.views.decorators.csrf import csrf_exempt


# Detail page (artwork) logic:
# Include Comment logic
@csrf_exempt
def artwork_detail(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)
    comment = Comment.objects.filter(aw_id_id=aw_id)
    reward = Reward.objects.filter(aw_id_id=aw_id)
    favourite = FavoriteRecord.objects.filter(aw_id_id=aw_id, customer_id_id=request.user.id)
    if request.method == 'POST':
        # Comment post
        form = CommentForm(request.POST)
        if 'commentButton' in request.POST:
            if form.is_valid():
                new_comment = Comment(
                    comment_time=datetime.now(),
                    comment_content=request.POST.get('comment_content'),
                    rating=request.POST.get('rating'),
                    aw_id_id=aw.id,
                    commenter_id_id=request.user.id,
                )
                new_comment.save()
                data = serializers.serialize('json',  Comment.objects.filter(aw_id_id=aw_id))
                return HttpResponse(json.dumps(data), content_type="application/json")
        # Favourite record post
        elif 'favouriteButton' in request.POST:
            # if not exists, add it to favourite list
            if favourite.count() == 0:
                new_favourite = FavoriteRecord(
                    fav_time=datetime.now(),
                    customer_id_id=request.user.id,
                    aw_id_id=aw_id
                )
                new_favourite.save()
            # if exists, delete the favourite record
            else:
                favourite.delete()
            return HttpResponseRedirect(reverse('aw', args=(aw.id,)))
    else:
        form = CommentForm()
    return render(request, "artwork/detail.html", {'form': form,
                                                   'aw': aw,
                                                   'comment': comment,
                                                   'reward': reward})


# Detail page (user) logic:
def artist_detail(request, user_id):
    user = get_object_or_404(UserProfile, user_id_id=user_id)
    aw = ArtWork.objects.filter(artist_id=user_id)
    return render(request, "artist/detail.html", {'user': user, 'aw': aw})


# Detail page (auction) logic:
def auction_detail(request, auction_id):
    auction_record = get_object_or_404(AuctionRecord, pk=auction_id)
    auction_history = AuctionHistory.objects.filter(ar_id_id=auction_id)
    return render(request, "auction/detail.html", {'record': auction_record, 'history': auction_history})


# Payment page (reward)
def reward_pay(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)

    # Reward post
    if request.method == 'POST':
        form = RewardForm(request.POST)
        if form.is_valid():
            new_reward = Reward(
                reward_time=datetime.now(),
                reward_amount=form.cleaned_data.get("reward_amount"),
                customer_id_id=request.user.id,
                aw_id_id=aw_id
            )
            new_reward.save()
            # PUT SUCCESS PAGE HERE LATER
            return HttpResponseRedirect(reverse('aw', args=(aw.id,)))
    else:
        form = RewardForm()
    return render(request, "artwork/reward.html", {'aw': aw, 'form': form})


# get comment list
def ajax_comment(request, aw_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = Comment(
            comment_time=datetime.now(),
            comment_content=request.POST.get('comment_content'),
            rating=request.POST.get('rating'),
            aw_id_id=aw_id,
            commenter_id_id=request.user.id,
        )
        new_comment.save()
    comment = Comment.objects.filter(aw_id_id=aw_id)
    data = serializers.serialize('json', comment)
    return HttpResponse(json.dumps(data), content_type="application/json")


# Auction creation page (reward)
def auction_creation(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)

    # Reward post
    if request.method == 'POST':
        form = AuctionCreateForm(request.POST)
        if form.is_valid():
            new_auction = AuctionRecord(
                ar_originalPrice=form.cleaned_data.get("ar_originalPrice"),
                ar_startTime=datetime.now(),
                ar_expiration=form.cleaned_data.get("ar_expiration"),
                ar_fixedPrice=form.cleaned_data.get("ar_fixedPrice"),
                aw_id_id=aw_id
            )
            new_auction.save()
            # PUT SUCCESS PAGE HERE LATER
            return HttpResponseRedirect(reverse('aw', args=(aw.id,)))
    else:
        form = AuctionCreateForm()
    return render(request, "artwork/auction.html", {'aw': aw, 'form': form})
