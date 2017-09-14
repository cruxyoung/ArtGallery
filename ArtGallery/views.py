from django.http import HttpResponse
from django.contrib.auth import login
from ArtGallery.forms import UserCreateForm
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from ArtGallery.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from ArtGallery.models import ArtWork, UserProfile, Comment, AuctionHistory, AuctionRecord


def hello(request):
    return HttpResponse("Hello world!")

# Sign up page
def signup(request):
    # Request to post a new data entry to database
    if request.method == 'POST':
        # Use embedded vertification system
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})


# Activation page logic
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


# Detail page (artwork) logic:
def artwork_detail(request, aw_id):
    aw = get_object_or_404(ArtWork, pk=aw_id)
    comment = Comment.objects.filter(aw_id_id=aw_id)
    return render(request, "artwork/detail.html", {'aw': aw, 'comment': comment})


# Detail page (user) logic:
def artist_detail(request, user_id):
    user = get_object_or_404(UserProfile, user_id_id=user_id)
    aw = ArtWork.objects.filter(artist_id=user_id)
    return render(request, "artist/detail.html", {'user': user, 'aw': aw})


# Detail page (comment) logic:
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    return render(request, "comment/detail.html",{'comment': comment})


# Detail page (auction) logic:
def auction_detail(request, auction_id):
    auction_record = get_object_or_404(AuctionRecord, pk=auction_id)
    auction_history = AuctionHistory.objects.filter(ar_id_id=auction_id)
    return render(request, "auction/detail.html", {'record': auction_record, 'history': auction_history})
