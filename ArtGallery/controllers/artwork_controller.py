import json
from django.http import HttpResponse
from django.core import serializers
from _datetime import datetime
from ArtGallery.forms import CommentForm, RewardForm, BidForm
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from ArtGallery.models import ArtWork, UserProfile, AuctionHistory, AuctionRecord, Comment, Reward, FavoriteRecord
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.models import User


# Detail page (artwork) logic:
# Include Comment logic
@csrf_exempt
@transaction.atomic
def artwork_detail(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)
    comment = Comment.objects.filter(aw_id_id=aw_id)
    reward = Reward.objects.filter(aw_id_id=aw_id)
    favourite = FavoriteRecord.objects.filter(aw_id_id=aw_id, customer_id_id=request.user.id)
    profile = get_object_or_404(UserProfile, pk=request.user.id)

    # get auction status for current user
    auction_list = AuctionHistory.objects.filter(customer_id_id=request.user.id)
    if auction_list.count() > 0:
        auction_record = auction_list.latest('ah_aucTime')
    else:
        auction_record = AuctionHistory (ah_remaining=3, ah_amount=0.01)
    form = CommentForm()
    bid_form = BidForm()
    reward_form = RewardForm()
    if request.method == 'POST':
        # Favourite record post
        if 'favouriteButton' in request.POST:
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
    if profile.identity == True:  # customer
        return render(request, "artwork/detail.html", {'form': form,
                                                       'aw': aw,
                                                       'comment': comment,
                                                       'reward': reward,
                                                       'bid': bid_form,
                                                       'auction_record': auction_record,
                                                       'identity': True,
                                                       'reward_form': reward_form
                                                   })
    else:  # artist
        return render(request, "artwork/detail.html", {'form': form,
                                                       'aw': aw,
                                                       'comment': comment,
                                                       'auction_record': auction_record,
                                                       'reward': reward,
                                                       'identity': False,
                                                       })


# Detail page (user) logic:
@transaction.atomic
@csrf_exempt
def artist_detail(request, user_id):
    user = get_object_or_404(UserProfile, user_id_id=user_id)
    aw = ArtWork.objects.filter(artist_id=user_id)
    return render(request, "artist/detail.html", {'user': user, 'aw': aw})


# Detail page (auction) logic:
@transaction.atomic
@csrf_exempt
def auction_detail(request, auction_id):
    auction_record = get_object_or_404(AuctionRecord, pk=auction_id)
    auction_history = AuctionHistory.objects.filter(ar_id_id=auction_id)
    return render(request, "auction/detail.html", {'record': auction_record, 'history': auction_history})


# Payment page (reward)
@transaction.atomic  # Ensure data integrity
@csrf_exempt
def ajax_reward(request, aw_id):
    form = RewardForm(request.POST)
    if form.is_valid():
        content = float(request.POST.get('reward_amount'))
        profile = get_object_or_404(UserProfile, user_id_id=request.user.id)
        balance = profile.amount
        if content < 1:
            return HttpResponse('{"status": "fail"}',
                                    content_type='application/json')
        elif balance < content:
            return HttpResponse('{"status": "balance"}',
                                content_type='application/json')
        else:
            new_reward = Reward(
                        reward_time=datetime.now(),
                        reward_amount=form.cleaned_data.get("reward_amount"),
                        customer_id_id=request.user.id,
                        aw_id_id=aw_id
                        )
            new_reward.save()
            # deduce the balance
            profile.amount = balance - content
            profile.save()
            reward = Reward.objects.filter(aw_id_id=aw_id)
            data = serializers.serialize('json', reward)
            return HttpResponse(json.dumps(data), content_type="application/json")


# get comment list
@transaction.atomic
@csrf_exempt
def ajax_comment(request, aw_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        content = request.POST.get('comment_content')
        if '/' in content or '$' in content or '<' in content:
            return HttpResponse('{"status": "fail", "msg": "For security reasons, '
                                'we does not allowed comments with special characteristics / and $."}',
                                content_type='application/json')
        else:
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


# send bid request
@transaction.atomic
@csrf_exempt
def ajax_bid(request, aw_id):
    form = BidForm(request.POST)
    record = AuctionHistory.objects.filter(customer_id_id=request.user.id)  # get all request list
    # If no record in the history, set the lowest price to 0, set the remaining times to 3
    if record.count() == 0:
        remaining = 3
        lowest_price = 0.0
    else:
        # find the remaining times and lowest price in record
        remaining = record.latest('ah_aucTime').ah_remaining
        lowest_price = record.latest('ah_aucTime').ah_amount
    ar_id = AuctionRecord.objects.filter(aw_id_id=aw_id).latest("id").id
    if form.is_valid():
        if remaining <= 0:
            return HttpResponse('{"status": "fail", "msg": "No more chance to bid this artwork."}',
                                content_type='application/json')
        else:
            new_history = AuctionHistory(
                ah_amount=request.POST.get('ah_amount'),
                ah_aucTime=datetime.now(),
                ar_id_id=ar_id,
                customer_id_id=request.user.id,
                ah_remaining=remaining - 1
            )
            if float(new_history.ah_amount) <= lowest_price:
                return HttpResponse('{"status": "fail", '
                                    '"msg": "The bid price should be higher than the price that your bid before"}',
                                    content_type='application/json')
            new_history.save()
            return HttpResponse('{"status": "success"}',
                                content_type='application/json')
