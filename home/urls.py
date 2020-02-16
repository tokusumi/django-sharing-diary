# mysite/home/urls.py

from django.urls import path, include

from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'home'

urlpatterns = [
    # ex: /
    path('', views.HomeView.as_view(), name='home'),
]
