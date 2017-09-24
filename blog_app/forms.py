from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.core.exceptions import ValidationError

from .models import Comment


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
        user = self.get_user()
        login(request, user)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

    def save(self, author, article, commit=True):
        if self.is_valid():
            comment = super(CommentForm, self).save(commit=False)
            comment.author = author
            comment.article_commented = article
            comment.save()
            return comment
        else:
<<<<<<< HEAD
            raise forms.ValidationError('Empty body of the comment')
=======
            raise ValidationError('Cannot add a new comment')
>>>>>>> new
