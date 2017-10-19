from django.http import HttpResponse
from django.contrib.auth import login
from ArtGallery.forms import UserCreateForm, UserProfileCreationForm
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from ArtGallery.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.db import transaction


# Sign up page
@transaction.atomic
def signup(request):
    # Request to post a new data entry to database
    if request.method == 'POST':

        # Use embedded authentication system
        form_user = UserCreateForm(request.POST)
        form_profile = UserProfileCreationForm(request.POST)
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            user.is_active = False
            user.save()

            profile = form_profile.save(commit=False)
            profile.is_active = False
            profile.user_id = user
            profile.id = user.id
            profile.save()

            current_site = get_current_site(request)
            message = render_to_string('registration/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your ArtGallery account.'
            to_email = form_user.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form_user = UserCreateForm()
        form_profile = UserProfileCreationForm()
    return render(request, 'registration/signup.html', {'form': form_user, 'profile': form_profile})


# Activation page logic
@transaction.atomic
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')