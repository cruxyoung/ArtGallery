from django.shortcuts import render, redirect
from.. import models
from django.http import HttpResponse


def personal_art_world(request, customer_id):
    customer = models.User.objects.get(pk=customer_id)
    return render(request, 'personal_center/personal_world.html', {'customer': customer})
