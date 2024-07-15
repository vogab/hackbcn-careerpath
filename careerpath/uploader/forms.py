from django import forms
from .models import UploadedImage, Request, Prompt

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['image', 'interests', 'skills', 'tone', 'prompt']


class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ['name', 'prompt']