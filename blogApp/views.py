from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from .models import Blog, Category,Comment
from django.db.models import Q
from django.http import HttpResponseRedirect

def posts_by_category(request, category_id):
    category = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    posts = Blog.objects.filter(status='published', category=selected_category).order_by('-id')

    # Pagination
    paginator = Paginator(posts, 3)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'category': category,
        'filter_posts': page_obj, 
        'selected_category': selected_category,
    }
    return render(request, 'category_posts.html', context)


def detail_blog(request,slug):
    category=Category.objects.all()
    single_post = get_object_or_404(Blog, slug=slug)
    comments=Comment.objects.filter(blog=single_post)
    comment_count=Comment.objects.filter(blog=single_post).count()
    if request.method=='POST':
        comment=Comment()
        comment.user=request.user
        comment.blog=single_post
        comment.comment=request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    context={
        'category':category,
        'single_post':single_post,
        'comments':comments,
        'comment_count':comment_count
    }
    return render(request,'single.html',context)

#search
def search(request):
    query = request.GET.get('query')
    category = Category.objects.all()
    results = []
    comments = []
    comment_count = 0

    if query:
        results = Blog.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query),
            status='published'
        )
        # Try to fetch a single post with exact slug match (if needed)
        try:
            single_post = Blog.objects.get(slug=query)
            comments = Comment.objects.filter(blog=single_post)
            comment_count = comments.count()
        except Blog.DoesNotExist:
            single_post = None

    context = {
        'results': results,
        'query': query,
        'category': category,
        'comment_count': comment_count,
        'comments': comments,
    }
    return render(request, 'search.html', context)

def view_all_post(request):
    all_posts=Blog.objects.all()
    category = Category.objects.all()

    context={
        'all_posts':all_posts,
        'category':category
    }
    return render(request,'blog_posts.html',context)



