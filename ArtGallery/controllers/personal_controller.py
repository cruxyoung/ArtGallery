import json
from django.http import HttpResponse
from django.shortcuts import render
from .. import models
from django.core.paginator import Paginator
from pure_pagination import Paginator
from pure_pagination import PageNotAnInteger
from django.views.generic.base import View
from .. import forms
from django.contrib.auth.hashers import make_password


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
                      'personal_center/personal_center_favorites.html',
                      {'customer': request.user,
                       'favs': favs_pag,
                       'favs_nums': favs_nums,
                       'sort': sort,
                       })


class PersonalAuction(View):
    # get auctions history of current user
    def get(self, request):
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


class PersonalReward(View):
    # get rewards history of current user
    def get(self, request):
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


class PersonalSetting(View):
    def get(self, request):
        user_profile = models.UserProfile.objects.get(user_id=request.user.id)
        return render(request,
                      'personal_center/personal_center_settings.html',
                      {'customer': request.user,
                       'user_profile': user_profile})

    def post(self, request):
        modify_form = forms.ModifyPwdForm(request.POST)
        user = request.user
        if modify_form.is_valid():
            pwd_ori = request.POST.get('password1', "")
            pwd_new = request.POST.get('password2', "")
            pwd_check = request.POST.get('password3', "")
            if pwd_new != pwd_check or '/' in pwd_check or '$' in pwd_check or '<' in pwd_check:
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


class UserInfoView(View):
    def post(self, request):
        user_info_form = forms.UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            valid_string = username + first_name + last_name
            if '/' in valid_string or '$' in valid_string or '<' in valid_string:
                return HttpResponse('{"status": "fail"}', content_type='application/json')
            else:
                user_info_form.save()
                return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class PersonalComplaint(View):
    # get complaints history of current user
    def get(self, request):
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


class DepositMoney(View):
    def post(self, request):
        user_profile = models.UserProfile.objects.get(user_id=request.user.id)
        deposit_money = float(request.POST.get('money', '0.0'))

        user_profile.amount += deposit_money
        user_profile.save()

        return HttpResponse('{"amount": ' + str(user_profile.amount) + '}', content_type='application/json')
