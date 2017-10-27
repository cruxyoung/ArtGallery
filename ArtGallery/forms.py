from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ArtGallery.models import Comment, Reward, UserProfile, AuctionHistory, ArtWork
from django.db import models


class UserCreateForm(UserCreationForm):
    email = forms.CharField(required=True)
    first_name = forms.CharField
    last_name = forms.CharField

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
        return user


class UserProfileCreationForm(forms.ModelForm):
    GENDER_CHOICES = (
        (True, "Male"),
        (False, "Female"),
    )
    IDENTITY_CHOICE = (
        (True, "Customer"),
        (False, "Artist"),
    )
    sex = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(attrs={'display': 'inline-block'}))
    birthday = forms.CharField(required=True, )
    identity = forms.ChoiceField(choices=IDENTITY_CHOICE, widget=forms.RadioSelect(attrs={'display': 'inline-block'}))

    class Meta:
        model = UserProfile
        fields = ("sex", "birthday", "identity")
        exclude = ['id']

    def save(self, commit=True):
        user_profile = super(UserProfileCreationForm, self).save(commit=False)
        user_profile.sex = self.cleaned_data["sex"]
        user_profile.birthday = self.cleaned_data["birthday"]
        user_profile.identity = self.cleaned_data["identity"]
        if commit:
            user_profile.save()
        return user_profile


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
    password3 = forms.CharField(required=True, min_length=5)


# should be modified later, cuz include userProfile
class UserInfoForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


# Form for post a comment to an artwork (artwork page)
class CommentForm(forms.ModelForm):
    comment_content = models.CharField(max_length=256)
    rating = models.FloatField(default=5.0)

    class Meta:
        model = Comment
        fields = ("rating", "comment_content")


# Form for reward an artwork (reward page)
class RewardForm(forms.ModelForm):
    reward_amount = models.FloatField

    class Meta:
        model = Reward
        fields = ("reward_amount",)


# Form to bid (artwork page)
class BidForm(forms.ModelForm):
    ah_amount = models.FloatField

    class Meta:
        model = AuctionHistory
        fields = ("ah_amount",)


# Form for Submit new artworks by artist
class ArtworkForm(forms.ModelForm):
    aw_name = forms.CharField(required=True)
    aw_location = forms.CharField(required=True)
    aw_type = forms.CharField()
    aw_genre = forms.CharField()
    aw_description = forms.CharField(max_length=256)
    aw_img = forms.ImageField(required=True)

    class Meta:
        model = ArtWork
        fields = ("aw_name", "aw_location", "aw_type", "aw_genre", "aw_description", "aw_img")


# Form for search the artwork
class SearchForm(forms.Form):
    filt = models.CharField(max_length=256)
