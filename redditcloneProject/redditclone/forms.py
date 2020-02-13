from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django_comments.models import Comment
from django.contrib.admin import widgets
from django_comments.forms import CommentForm                            

from .models import MPTTComment, Tread

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')       

class MPTTCommentForm(CommentForm):
    parent = forms.ModelChoiceField(queryset=MPTTComment.objects.all(), required=False, widget=forms.HiddenInput)
    name = forms.CharField(required=False, widget=forms.HiddenInput)
    url = forms.URLField(required=False, widget=forms.HiddenInput)
    email = forms.EmailField(required=False, widget=forms.HiddenInput)

    def get_comment_model(self):
        # Use our custom comment model instead of the built-in one.
        return MPTTComment

    def get_comment_create_data(self, **kwargs):
        # Use the data of the superclass, and add in the parent field field
        data = super(MPTTCommentForm, self).get_comment_create_data()
        data['parent'] = self.cleaned_data['parent']
        return data

class TreadForm(forms.Form):
    title = forms.CharField(required=True, max_length=100)
    comment = forms.CharField(required=False, widget=forms.Textarea, max_length=500)

    class Meta:
        model = Tread
        fields = ('title', 'comment')

class EditComment(forms.Form):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':4, 'cols': 50}))

    class Meta:
        model = Comment
        fields = ('comment')
