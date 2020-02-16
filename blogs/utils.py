# django imports
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from .models import Post, Category, Tag, Series


def get_category_all():
    cache_key = "{}-category-all".format(settings.CACHE_MIDDLEWARE_KEY_PREFIX)
    category = cache.get(cache_key)
    if category is None:
        try:
            category = Category.objects.all()
            cache.set(cache_key, category)
            return category
        except ObjectDoesNotExist:
            return None
    return category


def get_category_demo():
    cache_key = "{}-category-demo".format(settings.CACHE_MIDDLEWARE_KEY_PREFIX)
    category = cache.get(cache_key)
    if category is None:
        try:
            demo_posts = Post.objects.filter(author__username=settings.DEMO_USER)
            a = [str(qs.category) for qs in demo_posts]
            category = list(set(a))
            cache.set(cache_key, category)
            return category
        except ObjectDoesNotExist:
            return None
    return category


def get_tag_all():
    cache_key = "{}-tag-all".format(settings.CACHE_MIDDLEWARE_KEY_PREFIX)
    tag = cache.get(cache_key)
    if tag is None:
        try:
            tag = Tag.objects.all()
            cache.set(cache_key, tag)
            return tag
        except ObjectDoesNotExist:
            return None
    return tag


def get_tag_demo():
    cache_key = "{}-tag-demo".format(settings.CACHE_MIDDLEWARE_KEY_PREFIX)
    tag = cache.get(cache_key)
    if tag is None:
        try:
            demo_posts = Post.objects.filter(author__username=settings.DEMO_USER)
            a = [[str(tag) for tag in qs.tag.all()] for qs in demo_posts]
            from itertools import chain
            a = chain.from_iterable(a)
            tag = list(set(a))
            cache.set(cache_key, tag)
            return tag
        except ObjectDoesNotExist:
            return None
    return tag


def get_series_all():
    cache_key = "{}-series-all".format(settings.CACHE_MIDDLEWARE_KEY_PREFIX)
    series = cache.get(cache_key)
    if series is None:
        try:
            series = Series.objects.all()
            cache.set(cache_key, series)
            return series
        except ObjectDoesNotExist:
            return None
    return series
