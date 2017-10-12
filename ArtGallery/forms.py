from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ArtGallery.models import Comment, Reward
from django.db import models


class UserCreateForm(UserCreationForm):
    email = forms.CharField(required=True)
    first_name = forms.CharField
    last_name = forms.CharField

    class Meta:
        model = User
        fields = ("username", "email", "first_name","last_name","password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)
    password3 = forms.CharField(required=True, min_length=5)


# should be modified later, cuz include userProfile
class UserInfoForm(forms.ModelForm):
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
    reward_amount = models.FloatField(default=0.0)

    class Meta:
        model = Reward
        fields = ('reward_amount',)

