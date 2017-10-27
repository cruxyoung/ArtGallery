import json
from django.http import HttpResponse
from django.core import serializers
from _datetime import datetime
from ArtGallery.forms import CommentForm
from ArtGallery.forms import RewardForm
from ArtGallery.forms import BidForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import reverse
from ArtGallery.models import ArtWork
from ArtGallery.models import UserProfile
from ArtGallery.models import AuctionRecord
from ArtGallery.models import AuctionHistory
from ArtGallery.models import Comment
from ArtGallery.models import Complaint
from ArtGallery.models import Reward
from ArtGallery.models import FavoriteRecord

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Q


# Detail page (artwork) logic:
# Include Comment logic
@csrf_exempt
@transaction.atomic
def artwork_detail(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)
    comment = Comment.objects.filter(aw_id_id=aw_id)
    reward = Reward.objects.filter(aw_id_id=aw_id)
    favourite = FavoriteRecord.objects.filter(aw_id_id=aw_id, artist_id_id=request.user.id)
    favorite_stat = False if favourite.count() == 0 else True
    profile = get_object_or_404(UserProfile, pk=request.user.id)
    complaint = Complaint.objects.filter(aw_id=aw_id, customer_id=request.user.id)
    complaint_stat = True if complaint.count() > 0 else False
    bid = AuctionRecord.objects.filter(aw_id=aw_id)
    if bid.count() > 0:
        bid_stat = True
        num_bid = AuctionHistory.objects.filter(ar_id=bid[0].id).count()
        auction_list = AuctionHistory.objects.filter(customer_id_id=request.user.id, ar_id=bid[0].id)
    else:
        bid_stat = False
        num_bid = -1
        auction_list = None

    # get auction status for current user
    if auction_list == None:
        auction_record = None
    else:
        if auction_list.count() > 0:
            auction_record = auction_list.latest('ah_aucTime')
        else:
            auction_record = AuctionHistory(ah_remaining=3, ah_amount=bid[0].ar_originalPrice)
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
                    artist_id_id=request.user.id,
                    aw_id_id=aw_id
                )
                new_favourite.save()
            # if exists, delete the favourite record
            else:
                favourite.delete()
            return HttpResponseRedirect(reverse('aw', args=(aw.id,)))
    if profile.identity:  # customer
        return render(request, "artwork/detail.html", {'form': form,
                                                       'aw': aw,
                                                       'comment': comment,
                                                       'reward': reward,
                                                       'bid': bid_form,
                                                       'auction_record': auction_record,
                                                       'identity': True,
                                                       'reward_form': reward_form,
                                                       'favorite_stat': favorite_stat,
                                                       'complaint_stat': complaint_stat,
                                                       'bid_stat': bid_stat,
                                                       'num_bid': num_bid,
                                                       })
    else:  # artist
        return render(request, "artwork/detail.html", {'form': form,
                                                       'aw': aw,
                                                       'comment': comment,
                                                       'auction_record': auction_record,
                                                       'reward': reward,
                                                       'identity': False,
                                                       'favorite_stat': favorite_stat,
                                                       'complaint_stat': complaint_stat,
                                                       'bid_stat': bid_stat,
                                                       'num_bid': num_bid,
                                                       })


# Detail page (user) logic:
@transaction.atomic
@csrf_exempt
def artist_detail(request, user_id):
    user = get_object_or_404(UserProfile, user_id_id=user_id)
    aw = ArtWork.objects.filter(artist_id=user_id)
    return render(request, "artist/detail.html", {'user': user, 'aw': aw})


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
            # Modify artwork information
            profile.amount = balance - content
            aw = ArtWork.objects.get(pk=aw_id)
            aw.aw_totalAward += new_reward.reward_amount
            aw.save()

            new_reward.save()
            # deduce the balance
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
        rating = float(request.POST.get('rating'))
        if '/' in content or '$' in content or '<' in content:
            return HttpResponse('{"status": "fail"}',
                                content_type='application/json')
        elif rating < 1:
            return HttpResponse('{"status": "low_bound"}',
                                content_type='application/json')
        elif rating > 5:
            return HttpResponse('{"status": "high_bound"}',
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
            comments = Comment.objects.filter(aw_id_id=aw_id)
            data = serializers.serialize('json', comments)
            return HttpResponse(json.dumps(data), content_type="application/json")


# send bid request
@transaction.atomic
@csrf_exempt
def ajax_bid(request, aw_id):
    form = BidForm(request.POST)
    bid = AuctionRecord.objects.get(aw_id=aw_id)
    record = AuctionHistory.objects.filter(customer_id_id=request.user.id)  # get all request list
    # If no record in the history, set the lowest price to 0, set the remaining times to 3
    if record.count() == 0:
        remaining = 3
        lowest_price = bid.ar_originalPrice
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
                                    '"msg": "The bid price should be higher than your last bid and original price!"}',
                                    content_type='application/json')
            new_history.save()
            return HttpResponse('{"status": "success"}',
                                content_type='application/json')


@transaction.atomic
def complaints_edit(request, artwork_id):
    aw = ArtWork.objects.get(pk=artwork_id)
    complaint = Complaint.objects.filter(Q(aw_id=artwork_id, customer_id=request.user.id))
    complaint_stat = True if complaint.count() > 0 else False
    return render(request,
                  'artwork/aw_complaint.html',
                  {'aw': aw,
                   'complaint_stat': complaint_stat})


@transaction.atomic
# create complaint action
def complaints_action(request, artwork_id):
    complaint = Complaint.objects.filter(aw_id=artwork_id, customer_id=request.user.id)
    if complaint:
        return HttpResponseRedirect(reverse('customer_complaint'))
    else:
        # not write: fetch session customer_id
        complaint_type = request.POST.get('complaint_type', 'ILLEGAL')
        complaint_content = request.POST.get('complaint_content', 'COMPLAINTS')
        complaint_time = datetime.now()
        Complaint.objects.create(complaint_type=complaint_type, complaint_content=complaint_content,
                                 complaint_time=complaint_time, aw_id_id=artwork_id, customer_id=request.user)

        return HttpResponseRedirect(reverse('customer_complaint'))


@transaction.atomic
# cancel the created complaint record
def withdraw_complaints(request, artwork_id):
    for complaint in Complaint.objects.all():
        if complaint.aw_id_id == int(artwork_id):
            if complaint.customer_id_id == request.user.id:
                Complaint.objects.filter(id=complaint.id).delete()
                return HttpResponseRedirect(reverse('aw', args=(artwork_id,)))
