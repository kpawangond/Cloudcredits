from django.shortcuts import redirect, render,get_object_or_404
from blogApp.models import Blog,Category,Comment
from dashboards.forms import CategoryForm,PostForm,AddUserForm,EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# dashboards/decorators.py
from django.http import Http404
from functools import wraps

#function for role based access.
def staff_or_superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
            raise Http404("Page not found")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.
@login_required
@staff_or_superuser_required
def dashboard(request):
    catagory_counts=Category.objects.all().count()
    post_counts=Blog.objects.all().count()
    latest_posts=Blog.objects.filter(is_featured=False,status='published').order_by('-created_at')[:5]
    user_counts=User.objects.all().count()
    comment_conunts=Comment.objects.count()
 
    context={
        'catagory_counts':catagory_counts,
        'post_counts':post_counts,
        'latest_posts':latest_posts,
        'user_counts':user_counts,
        'comment_conunts':comment_conunts,
    }
    return render(request,'dashboard/admin_dashboard.html',context)

#category views function
@login_required
@staff_or_superuser_required
def categories_view(request):
    all_category=Category.objects.all()
    context={
        'all_category':all_category
    }
    return render(request,'dashboard/view_category.html',context)


#add Category
@login_required
@staff_or_superuser_required
def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)
        print(form)
        if form.is_valid():
          form.save()
          return redirect('categories_view')
    else:    
        form=CategoryForm()    
    context={
        'form':form
    }
    return render(request,'dashboard/add-category.html',context)


# Edit Category View
@login_required
@staff_or_superuser_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories_view') 
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'dashboard/edit-category.html', context)

#Delete category
@login_required
@staff_or_superuser_required
def delete_category(request,pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories_view')

#Post views function
@login_required
@staff_or_superuser_required
def post_view(request):
    all_post=Blog.objects.all()
    context={
        'all_post':all_post
    }
    return render(request,'dashboard/view_post.html',context)

def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while Blog.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

#Add Post
@login_required
@staff_or_superuser_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Use title from cleaned_data (not changed_data)
            title = form.cleaned_data.get('title')
            post.slug = generate_unique_slug(title)

            post.save()
            return redirect('post_view')
    else:
        form = PostForm() 
    context={
        'form':form
    }
    return render(request,'dashboard/add-post.html',context)

#update slug
def generate_unique_slug(title, instance_id=None):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while Blog.objects.filter(slug=slug).exclude(pk=instance_id).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

# Update Post View
@login_required
@staff_or_superuser_required
def update_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            new_title = form.cleaned_data.get('title')
            updated_post.slug = generate_unique_slug(new_title, instance_id=post.pk)

            updated_post.save()
            return redirect('post_view')
    else:
        form = PostForm(instance=post)

    return render(request, 'dashboard/edit-post.html', {'form': form, 'post': post})
 

 #Delete category
@login_required
@staff_or_superuser_required
def delete_post(request,pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('post_view')

@login_required
@staff_or_superuser_required
def detail_post(request,pk):
    post_details = get_object_or_404(Blog, pk=pk)
    context={
        'post_details':post_details
    }
    return render(request,'dashboard/details-post.html',context)

#user function
@login_required
@staff_or_superuser_required
def users_view(request):
    users=User.objects.all()
    context={
        'users':users
    }
    return render(request,'dashboard/users-view.html',context)

@login_required
@staff_or_superuser_required
def add_user(request):
    if request.method=='POST':
        form=AddUserForm(request.POST)
        print(form)
        if form.is_valid():
          form.save()
          return redirect('users')
    else:    
        form=AddUserForm()    
    context={
        'form':form
    }
    return render(request,'dashboard/add_user.html',context)

#Edit users
@login_required
@staff_or_superuser_required
def update_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users') 
    else:
        form = EditUserForm(instance=user)
    
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'dashboard/edit-user.html', context)

#delete user
@login_required
@staff_or_superuser_required
def delete_user(request,pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')  

@login_required
@staff_or_superuser_required
def profile_view(request):
    return render(request, 'dashboard/users-profile.html')
  

def custom_404_view(request, exception):
    return render(request, 'dashboard/page-404.html', status=404)