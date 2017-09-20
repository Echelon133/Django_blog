from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login


class UserSignupForm(UserCreationForm):
    username = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        new_user = super(UserSignupForm, self).save(commit=False)
        new_user.username = self.cleaned_data['username']

        user = User.objects.filter(username=new_user.username) 
        if not user and commit:
            # if user with specified username doesn't exist 
            new_user.save()
        return new_user


class UserLoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')

    def login(self):
        self.clean()
        request = self.request
        user = self.user_cache
        login(request, user)