import json
from .. import forms
from .. import models
from _datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.shortcuts import HttpResponseRedirect, reverse
from django.db.models import Q


class ArtistArtwork(View):
    # get all artworks related information created by current artist user
    def get(self, request):
        artworks = models.ArtWork.objects.filter(Q(artist_id=request.user.id))
        return render(request,
                      'personal_center/artist_center_artworks.html',
                      {'customer': request.user,
                       'artworks': artworks})


class ArtworkEdit(View):
    def get(self, request, artwork_id):
        if str(artwork_id) == '0':
            return render(request,
                          'personal_center/artist_center_edit.html',
                          {'customer': request.user})
        else:
            artwork = models.ArtWork.objects.get(pk=artwork_id)
            return render(request,
                          'personal_center/artist_center_edit.html',
                          {'customer': request.user,
                           'artwork': artwork})


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
                    aw_auctionStat=request.POST.get('aw_auction'),
                    aw_description=request.POST.get('aw_description'),
                    aw_img=add_form.cleaned_data['aw_img'],
                    artist_id=request.user,
                    aw_time=datetime.now(),
                    aw_totalAward=0.0,
                )

                # Create new information in auction history if auctionStat == 1
                # if request.POST.get('aw_auction'):
                #     start_time = request.POST.get('auctionStart')
                #     end_time = request.POST.get('auctionEnd')
                #     time_period = datetime(end_time) - datetime(start_time)

                # return HttpResponse('{"status": "success", "id":' + str(new_artwork.id) + '}',
                #                     content_type='application/json')

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
                artwork.aw_auctionStat = request.POST.get('aw_auction')
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


class UploadImage(View):
    def post(self, request, artwork_id):
        image_form = forms.UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            artwork = models.ArtWork.objects.get(Q(pk=artwork_id))
            image = image_form.cleaned_data['aw_img']
            artwork.aw_img = image
            artwork.save()


# class DeleteArtwork(View):
def delete_artwork(request, artwork_id):
    models.ArtWork.objects.get(Q(pk=artwork_id)).delete()

    return HttpResponseRedirect('/artist/artworks')


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
