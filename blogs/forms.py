from django import forms
from .models import Comment, Post, Category, Tag, Series, Pictures


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author", "body")


class SearchForm(forms.ModelForm):
    word = forms.CharField(max_length=10)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "image", "series", "category", "tag", "body", "is_public", "notification",)


class PostImageForm(forms.ModelForm):
    # body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = ("image",)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ("name",)


class PicturesForm(forms.ModelForm):
    class Meta:
        model = Pictures
        fields = ("image",)
