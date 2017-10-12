import json
from .. import forms
from .. import models
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password


class ArtistArtwork(View):
    # get all artworks related information created by current artist user
    def get(self, request):
        artworks = models.ArtWork.objects.filter(artist_id=request.user.id)
        return render(request,
                      'personal_center/artist_center_artworks.html',
                      {'customer': request.user,
                       'artworks': artworks})


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