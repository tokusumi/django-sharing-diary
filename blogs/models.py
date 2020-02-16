from django.db import models
from django.conf import settings
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.html import strip_tags
import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.db.models import signals
from django.core.mail import send_mail
from django.template import loader


class Category(models.Model):
    name = models.CharField('Category', max_length=255)
    created_at = models.DateTimeField('created time', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_latest_post(self):
        result = Post.objects.filter(category__parent=self).filter(is_public=True).order_by('-created_at')[:5]
        return result

    def public_counter(self):
        count = self.post_set.filter(is_public=True).count()
        return count

    def get_absolute_url(self):
        return reverse('blogs:index')


class Tag(models.Model):
    name = models.CharField('Tag', max_length=255)
    created_at = models.DateTimeField('created time', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_latest_post(self):
        result = Post.objects.filter(tag=self).filter(is_public=True).order_by('-created_at')[:5]
        return result

    def get_absolute_url(self):
        return reverse('blogs:index')


class Series(models.Model):
    name = models.CharField('Series', max_length=255)
    created_at = models.DateTimeField('created time', auto_now_add=True)

    def __str__(self):
        return self.name

    def get_latest_post(self):
        result = Post.objects.filter(series__parent=self).filter(is_public=True).order_by('-created_at')[:5]
        return result

    def public_counter(self):
        count = self.post_set.filter(is_public=True).count()
        return count

    def get_absolute_url(self):
        return reverse('blogs:index')


class Pictures(models.Model):
    image = ProcessedImageField(
        upload_to="uploads/%Y/%m/%d/",
        null=False,
        blank=False,
        processors=[ResizeToFill(830, 580)], format="JPEG", options={'quality': 90},
        verbose_name="Picture"
    )
    thumbnail = ProcessedImageField(
        upload_to="",
        null=True,
        blank=True,
        processors=[ResizeToFill(75, 75)], format="JPEG", options={'quality': 90},
    )

    def save(self, *args, **kwargs):
        super(Pictures, self).save(*args, **kwargs)
        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

    def make_thumbnail(self):
        image = Image.open(self.image)
        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        # thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension
        temp_thumb = BytesIO()
        image.save(temp_thumb, 'JPEG')  # file objectをstring形式として、contentfileに保存
        # You need to seek back to the beginning of the file after writing the initial in memory file...
        temp_thumb.seek(0)
        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
        return True

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return reverse('blogs:index')


class Post(models.Model):
    title = models.CharField("Title", max_length=255, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, verbose_name="Author",
        blank=True, null=True,
    )
    image = ProcessedImageField(
        upload_to="blogs/post_img/%y/%m/%d/",
        null=True,
        blank=True,
        processors=[ResizeToFill(830, 580)], format="JPEG", options={'quality': 90},
        verbose_name="Featured image"
    )
    series = models.ForeignKey(Series, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Series")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Category")
    tag = models.ManyToManyField(Tag, blank=True, verbose_name="Tags")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = RichTextUploadingField("Body", blank=True, null=True,)
    is_public = models.BooleanField('公開設定', default=False,)
    notification = models.BooleanField('通知設定', default=False,)

    def __str__(self):
        return self.title

    def summary(self):
        return strip_tags(self.body)[:30]

    def long_summary(self):
        return strip_tags(self.body)[:150]

    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True, null=True,
    )
    created_at = models.DateTimeField('投稿日', auto_now_add=True)
    body = models.TextField('本文', max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.author


def notify_admin(sender, instance, created, **kwargs):
    '''Notify the administrator that a new post has been added.'''
    if instance.notification:
        if settings.EMAIL_BY and settings.EMAIL_TO:
            subject = 'New post from %s !!!' % instance.author
            mail_template = loader.get_template('blogs/post-notification.txt')
            context = {
                "post": instance,
                "base_url": settings.BASE_URL
            }
            message = mail_template.render(context)
            from_addr = settings.EMAIL_BY
            recipient_list = settings.EMAIL_TO
            send_mail(subject, message, from_addr, recipient_list)


signals.post_save.connect(notify_admin, sender=Post)


def notify_admin_comment(sender, instance, created, **kwargs):
    '''Notify the administrator that a new post has been added.'''
    if settings.EMAIL_BY and settings.EMAIL_TO:
        subject = 'New comment from %s !!!' % instance.author
        mail_template = loader.get_template('blogs/comment-notification.txt')
        context = {
            "post": instance,
            "base_url": settings.BASE_URL
        }
        message = mail_template.render(context)
        from_addr = settings.EMAIL_BY
        recipient_list = settings.EMAIL_TO
        send_mail(subject, message, from_addr, recipient_list)


signals.post_save.connect(notify_admin_comment, sender=Comment)
