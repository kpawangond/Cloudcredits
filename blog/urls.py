from django.contrib import admin
from django.urls import path,include, re_path
from blog.views import home, register,login_view,logout_view
from django.conf.urls.static import static
from django.conf import settings
from blogApp.views import detail_blog,search,view_all_post
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('category/',include('blogApp.urls')),
    path('<slug:slug>',detail_blog,name='detail_blog'),
    path('blogs/search',search,name='search'),
    path('register/',register,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('blog_posts/',view_all_post,name="view_all_post"),
    path('dashboard/',include('dashboards.urls')),

]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT,
        }),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

# page 404 error handler
handler404 = 'dashboards.views.custom_404_view'