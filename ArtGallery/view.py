from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, redirect
from.import models


def hello(request):
    return HttpResponse("Hello world!")


# Sign up page
def signup(request):
    # Request to post a new data entry to database
    if request.method == 'POST':
        # Use embedded verification system
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


def index_ignore(request):
    art_customers = models.User.objects.all()

    return render(request, 'home/index.html', {'art_customers': art_customers})

