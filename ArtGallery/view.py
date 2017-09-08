from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render
from django.shortcuts import redirect
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


# Log in test session
# def login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         pwd = request.POST.get('pws')
#         user = auth.authenticate(username=username, password=pwd)
#         if user is not None and user.is_active:
#             request.session['IS_LOGIN'] = True
#             return request(request, 'home/index.html')


def index_ignore(request):
    # get Session
    # username = request.session['username']

    if request.user.is_authenticated():
        customer = request.user
        return render(request, 'home/index.html', {'customer': customer})

    else:
        return render(request, 'home/index.html')

