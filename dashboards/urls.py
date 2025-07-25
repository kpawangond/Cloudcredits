from django.urls import path
from dashboards.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',dashboard,name='dashboard'),
    
    #urls for Category
    path('view_category/',categories_view,name="categories_view"),
    path('category/add/',add_category,name='add_category'),
    path('category/edit/<int:pk>/',update_category,name='edit_category'),
    path('category/delete/<int:pk>/',delete_category,name="delete_category"),

    #urls for Post
    path('view_post/',post_view,name='post_view'),
    path('post/add/',add_post,name='add_post'),
    path('post/edit/<int:pk>/',update_post,name='edit_post'),
    path('post/delete/<int:pk>/',delete_post,name='delete_post'),
    path('post/detail/<int:pk>/',detail_post,name='detail_post'),

    #urls for user
    path('users/',users_view,name='users'),
    path('users/add/',add_user,name='add_user'),
    path('users/edit/<int:pk>/',update_user,name='edit_user'),
    path('users/delete/<int:pk>',delete_user,name="delete_user"),
    path('profile/', profile_view, name='profile'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)