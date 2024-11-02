from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Project, Comment


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'cover_image']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autocomplete'] = 'off'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'file']  # Поля для отображения в форме
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Добавьте комментарий...', 'rows': 4, 'cols': 40}),
        }
