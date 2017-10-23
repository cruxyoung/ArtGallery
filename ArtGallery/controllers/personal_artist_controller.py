import json
from .. import forms
from .. import models
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.shortcuts import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from pure_pagination import Paginator, PageNotAnInteger


class ArtistArtwork(View):
    # get all artworks related information created by current artist user
    def get(self, request):
        artworks = models.ArtWork.objects.filter(Q(artist_id=request.user.id))

        return render(request,
                      'personal_center/artist_center_artworks.html',
                      {'customer': request.user,
                       'artworks': artworks,
                       })


class ArtworkEdit(View):
    def get(self, request, artwork_id):
        if str(artwork_id) == '0':
            return render(request,
                          'personal_center/artist_center_edit.html',
                          {'customer': request.user})
        else:
            artwork = models.ArtWork.objects.get(pk=artwork_id)
            if artwork.aw_auctionStat:

                return render(request,
                              'personal_center/artist_center_edit.html',
                              {'customer': request.user,
                               'artwork': artwork,
                               })
            else:
                return render(request,
                              'personal_center/artist_center_edit.html',
                              {'customer': request.user,
                               'artwork': artwork,
                               })


def delete_artwork(request, artwork_id):
    models.ArtWork.objects.get(Q(pk=artwork_id)).delete()

    return HttpResponseRedirect('/artist/artworks')


class EditAction(View):
    def post(self, request):
        artworks = models.ArtWork.objects.filter(Q(artist_id=request.user.id))
        artwork_id = request.POST.get('artwork_id', '0')
        if str(artwork_id) == '0':
            add_form = forms.ArtworkForm(request.POST, request.FILES)
            if add_form.is_valid():
                models.ArtWork.objects.create(
                    aw_name=request.POST.get('aw_name'),
                    aw_location=request.POST.get('aw_location'),
                    aw_type=request.POST.get('aw_type'),
                    aw_genre=request.POST.get('aw_genre'),
                    aw_auctionStat=0,
                    aw_description=request.POST.get('aw_description'),
                    aw_img=add_form.cleaned_data['aw_img'],
                    artist_id=request.user,
                    aw_time=datetime.now(),
                    aw_totalAward=0.0
                )

                return render(request,
                              'personal_center/artist_center_artworks.html',
                              {'customer': request.user,
                               'artworks': artworks,
                               'result': 'Adding Successfully'})
            else:
                return render(request,
                              'personal_center/artist_center_artworks.html',
                              {'customer': request.user,
                               'artworks': artworks,
                               'result': 'Adding Failed'})
        else:
            edit_form = forms.ArtworkForm(request.POST, request.FILES)
            if edit_form.is_valid():
                artwork = models.ArtWork.objects.get(Q(pk=artwork_id))
                artwork.aw_name = request.POST.get('aw_name')
                artwork.aw_location = request.POST.get('aw_location')
                artwork.aw_type = request.POST.get('aw_type')
                artwork.aw_genre = request.POST.get('aw_genre')
                artwork.aw_description = request.POST.get('aw_description')
                artwork.aw_img = edit_form.cleaned_data['aw_img']

                artwork.save()

                return render(request,
                              'personal_center/artist_center_artworks.html',
                              {'customer': request.user,
                               'artworks': artworks,
                               'result': 'Editing Successfully'})
            else:
                return render(request,
                              'personal_center/artist_center_artworks.html',
                              {'customer': request.user,
                               'artworks': artworks,
                               'result': 'Editing Failed'})


# Auction Operation
class ArtworkAuction(View):
    def get(self, request, artwork_id):
        # artwork = models.ArtWork.objects.get(Q(pk=artwork_id))
        auction_record = models.AuctionRecord.objects.get(Q(aw_id=artwork_id))
        # Convert datetime to string in order to put it at input widget
        auction_record.ar_time = auction_record.ar_time.strftime("%Y-%m-%dT%H:%M")
        auction_record.ar_end_time = auction_record.ar_end_time.strftime("%Y-%m-%dT%H:%M")
        auction_histories = models.AuctionHistory.objects.filter(Q(ar_id=auction_record.id))
        return render(request,
                      'personal_center/artist_center_auctions.html',
                      {'customer': request.user,
                       # 'artwork': artwork,
                       'auction_record': auction_record,
                       'auction_histories': auction_histories
                       })

    def post(self, request, artwork_id):
        # Create new information in auction history if auctionStat == 1
        if request.POST.get('aw_auction') == '1':
            artwork = models.ArtWork.objects.get(Q(pk=artwork_id))
            start_time = datetime.strptime(request.POST.get('auctionStart'), "%Y-%m-%dT%H:%M")
            end_time = datetime.strptime(request.POST.get('auctionEnd'), "%Y-%m-%dT%H:%M")

            original_price = float(request.POST.get('ar_originalPrice'))

            artwork.aw_auctionStat = 1
            models.AuctionRecord.objects.create(
                ar_originalPrice=original_price,
                ar_time=start_time,
                ar_end_time=end_time,
                aw_id=artwork
            )
            artwork.save()

            artworks = models.ArtWork.objects.filter(Q(artist_id=request.user.id))
            return render(request,
                          'personal_center/artist_center_artworks.html',
                          {'customer': request.user,
                           'artworks': artworks,
                           'result': 'Open Auction Successfully'})
        else:
            return HttpResponseRedirect('/artist/artworks')

    def delete(self, request, artwork_id):
        pass


class ArtworkReward(View):
    def get(self, request, artwork_id):
        reward_histories = models.Reward.objects.filter(Q(aw_id=artwork_id))
        artwork = models.ArtWork.objects.get(Q(pk=artwork_id))
        return render(request,
                      'personal_center/artist_center_rewards.html',
                      {'customer': request.user,
                       'artwork': artwork,
                       'reward_histories': reward_histories})


class ArtistSetting(View):
    # get personal information of current artist user
    def get(self, request):
        return render(request,
                      'personal_center/artist_center_settings.html',
                      {'customer': request.user})

    def post(self, request):
        modify_form = forms.ModifyPwdForm(request.POST)
        user = request.user
        if modify_form.is_valid():
            pwd_ori = request.POST.get('password1', "")
            pwd_new = request.POST.get('password2', "")
            pwd_check = request.POST.get('password3', "")
            if pwd_new != pwd_check:
                return HttpResponse('{"status": "fail", "msg": "New Password Not Match."}',
                                    content_type='application/json')
            if user.check_password(pwd_ori):
                user.password = make_password(pwd_new)
                user.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "wrong", "msg": "Not match current password."}')

        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


# Artist favorite
class PersonalFavorite(View):
    # get favorites of current user
    def get(self, request):

        favs = models.FavoriteRecord.objects.filter(artist_id=request.user.id)
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
                      'personal_center/artist_center_favorites.html',
                      {'customer': request.user,
                       'favs': favs_pag,
                       'favs_nums': favs_nums,
                       'sort': sort,
                       })


# Artist Comment
class PersonalComment(View):
    # get comments history of current user
    def get(self, request):
        comments = models.Comment.objects.filter(commenter_id=request.user.id)
        comments_nums = comments.count()

        # get sort info
        sort = request.GET.get('sort', "")
        if sort:
            if sort == 'time':
                comments = comments.order_by('-comment_time')
            if sort == 'comment':
                comments = comments.filter(reply_commentId=None)
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
                      'personal_center/artist_center_comments.html',
                      {'customer': request.user,
                       'comments': comments_pag,
                       'comments_nums': comments_nums,
                       'sort': sort,
                       })
