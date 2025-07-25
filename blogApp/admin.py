from django.contrib import admin
from blogApp.models import Category,Blog,Comment
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','category_name','created_at','updated_at')

admin.site.register(Category,CategoryAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display=('id','title','category','status','created_at')
    prepopulated_fields = {'slug': ('title',)} 

admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
