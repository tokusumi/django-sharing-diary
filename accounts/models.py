from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class MyUser(AbstractUser):
    ###followings are predefined
    # EMAIL_FIELD = 'email'
    # USERNAME_FIELD = 'username'
    location = models.CharField('location', max_length=30, blank=True)
    # gender =
    birth_date = models.DateField('birth date', null=True, blank=True)
    avatar =ProcessedImageField(upload_to="accounts/avatar_img/%y/%m/%d/", null=True, blank=True, processors=[ResizeToFill(100,100)],format="JPEG",options={'quality': 90})
    REQUIRED_FIELDS = ['email', 'birth_date'] # add 必須項目
