from .models import Post, Tag, Category, Series, Pictures
from imagekit.cachefiles import ImageCacheFile
from imagekit.processors import ResizeToFill
from imagekit import ImageSpec
from imagekit.admin import AdminThumbnail
from django.contrib import admin
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdminThumbnailSpec(ImageSpec):
    processors = [ResizeToFill(80, 80)]
    format = 'JPEG'
    options = {'quality': 90}


def cached_admin_thumb(instance):
    if instance.image:
        # `image` is the name of the image field on the model
        cached = ImageCacheFile(AdminThumbnailSpec(instance.image))
        # only generates the first time, subsequent calls use cache
        cached.generate()
        return cached
    else:
        return None


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'admin_thumb', 'title', 'author', 'created_at', 'updated_at',
                    'is_public', 'series', '_tag', 'category', 'summary')  # 一覧に出したい項目
    list_display_links = ('title', 'is_public', 'category', '_tag',)  # 修正リンクでクリックできる項目
    if cached_admin_thumb:
        admin_thumb = AdminThumbnail(image_field=cached_admin_thumb)

    def _tag(self, row):
        return ','.join([x.name for x in row.tag.all()])


admin.site.register(Post, PostAdmin)


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


admin.site.register(Series, SeriesAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')  # 一覧に出したい項目
    list_display_links = ('name',)  # 修正リンクでクリックできる項目


admin.site.register(Tag, TagAdmin)


class PicturesAdmin(admin.ModelAdmin):
    list_display = ('id', 'image',)  # 一覧に出したい項目
    list_display_links = ('image',)  # 修正リンクでクリックできる項目


admin.site.register(Pictures, PicturesAdmin)
