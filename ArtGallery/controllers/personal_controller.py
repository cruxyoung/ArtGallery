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
    complaints = models.Complaint.objects.filter(customer_id=request.user.id).select_related('aw_id')
    return render(request,
                  'personal_center/personal_center_complaints.html',
                  {'complaints': complaints,
                   'customer': request.user},
                  )

#
# def personal_show_category(request):
#     customer = request.user
#     # setting_data = {'MENU': ('Information', 'Security'),
#     #                 'CONTENT': {'username': customer.username, "sex": "Male"}}
#     setting_data = {'MENU': {'INFORMATION': {'username': customer.username,
#                                              'last_login': str(customer.last_login),
#                                              'first_name': customer.first_name,
#                                              'last_name': customer.last_name,
#                                              'email': customer.email},
#                              'SECURITY': {'password': customer.password,
#                                           'account': 0.0}}}
#
#     json_data = json.dumps(setting_data)
#
#     return HttpResponse(json_data)
#     # return JsonResponse(json_data)



