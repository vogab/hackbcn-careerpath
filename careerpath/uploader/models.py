from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

possible_tones = [
    (1, 'Formal'),
    (2, 'Casual'),
    (3, 'Playful')
]

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.pk}"


class Request(models.Model):
    # Tone: 1 = Casual, 2 = Business Casual, 3 = Business Professional
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tone = models.IntegerField(choices=possible_tones, default=1)
    interests = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    prompt = models.ForeignKey('Prompt', on_delete=models.SET_NULL, blank=True, null=True)
    response = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Request {self.pk}"
    
    def save(self, *args, **kwargs):
        # Resize image
        if self.image:
            img = Image.open(self.image)
            if img.height > 600 or img.width > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)

                # Save the resized image
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)

        super().save(*args, **kwargs)
    

class Prompt(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()
    

    def __str__(self):
        return f"Prompt {self.pk}: {self.name}"
