from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Comment, Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "python, django, venv" }),
    )

    class Meta:
        model = Post
        fields = ("title", "body", "is_published")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post sarlavhasi"}),
            "body": forms.Textarea(
                attrs={"rows": 14, "placeholder": "Postingizni shu yerga yozing..."}
            ),
        }

    def clean_tags(self):
        names = []
        for part in self.cleaned_data["tags"].split(","):
            name = part.strip().lstrip("#").lower()
            if not name:
                continue
            if len(name) > 45:
                raise forms.ValidationError("Har bir teg 45 belgidan oshmasin.")
            if not slugify(name):
                raise forms.ValidationError(f"'{name}' teg sifatida yaroqsiz.")
            if name not in names:
                names.append(name)
        return names

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Fikringizni yozing..."}
            ),
        }