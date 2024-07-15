from django.contrib import admin
from .models import UploadedImage, Request, Prompt


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'uploaded_at']


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__', 'uploaded_at', 'tone', 'response']
    # list_display = ['pk', 'image']


@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'prompt']