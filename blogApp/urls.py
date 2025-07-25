from django.urls import path
from blogApp.views import *


urlpatterns = [
    path('<int:category_id>/',posts_by_category,name="posts_by_category"),
]