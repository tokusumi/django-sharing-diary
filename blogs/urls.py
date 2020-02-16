# accountapp/blogs/urls.py

from django.urls import path

from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'blogs'

urlpatterns = [
    # ex: /
    path('', views.IndexView.as_view(), name='index'),
    # ex: /blogs/create/
    path('create/', views.CreateView.as_view(), name='create'),
    # ex: /blogs/1/
    path('editlist/', views.EditListView.as_view(), name='editlist'),

    path('<int:pk>/', views.PostDetailFormView.as_view(), name='detail'),
    # ex: /blogs/1/update/
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name='update'),
    # ex: /blogs/ajax/1/update/ for ajax asynchronized post
    path('<int:pk>/update/ajax', views.PostUpdateView.as_view(), name='update-ajax'),
    # asynchronized image, tag, caegory, series
    path('<int:pk>/update/ajax/image/', views.PostImageView.as_view(), name='update-ajax-image'),
    path('ajax/add_tags/', views.AddTagView.as_view(), name='add-tag'),
    path('ajax/add-category/', views.AddCategoryView.as_view(), name='add-category'),
    path('ajax/add_series/', views.AddSeriesView.as_view(), name='add-series'),
    path('ajax/add_pictures/', views.AddPicturesView.as_view(), name='add-pictures'),

    # ex: /blogs/1/delete
    path('<int:pk>/delete/', views.DeleteView.as_view(), name='delete'),

]
