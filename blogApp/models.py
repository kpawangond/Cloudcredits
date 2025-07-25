from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=100,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural='Categories'

    def __str__(self):
        return self.category_name   


STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)


class Blog(models.Model):
    title=models.CharField(max_length=150,unique=True)
    slug=models.SlugField(unique=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    author=models.ForeignKey(User, on_delete=models.CASCADE)   
    image=models.ImageField(upload_to='uploads')
    description=models.TextField(max_length=2000)
    content=models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') 
    is_featured=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment=models.TextField(max_length=250)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment
