from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PostForm

from django.contrib.auth import login, logout
from .models import Post, Category



# def home(request):
#     categories = Category.objects.all()
#     posts = Post.objects.all()
#     user = request.user
#     return render(request, 'mediaApp/home.html', {'user':user,'categories': categories, 'posts' : posts})



def home(request):
    # Get all categories for the sidebar
    categories = Category.objects.all()
    
    # Initialize query for posts
    posts = Post.objects.all()
    
    # Filtering by category
    category_name = request.GET.get('category', '')
    if category_name:
        posts = posts.filter(category__name=category_name)
    
    # Filtering by author
    author = request.GET.get('author', '')
    if author:
        posts = posts.filter(user__username__icontains=author)
    
    # Filtering by keyword (search in title or description)
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = posts.filter(title__icontains=keyword) | posts.filter(description__icontains=keyword)
    
    # Sorting by date (newest or oldest)
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'newest':
        posts = posts.order_by('-created_at')
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')
    
    # Return the filtered posts to the template
    return render(request, 'mediaApp/home.html', {'posts': posts, 'categories': categories})

# def category_posts(request, category_name):
#     category = get_object_or_404(Category, name=category_name)
#     posts = Post.objects.filter(category=category)
#     categories = Category.objects.all()
#     return render(request, 'mediaApp/home.html', {'posts': posts, 'categories': categories, 'selected_category': category_name})

def category_posts(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    categories = Category.objects.all()

    # Filtering by author
    author = request.GET.get('author', '')
    if author:
        posts = posts.filter(user__username__icontains=author)

    # Filtering by keyword
    keyword = request.GET.get('keyword', '')
    if keyword:
        posts = posts.filter(title__icontains=keyword) | posts.filter(description__icontains=keyword)

    # Sorting by date
    sort_by = request.GET.get('sort_by', '')
    if sort_by == 'newest':
        posts = posts.order_by('-created_at')
    elif sort_by == 'oldest':
        posts = posts.order_by('created_at')
    
    return render(request, 'mediaApp/home.html', {'posts': posts, 'categories': categories, 'selected_category': category_name})

@login_required
def base_view(request):
    users = request.user
    # print(users, users.id)
    pos = Post.objects.get(user_id = request.id)
    if pos.exists():
        pos = pos.first()  # Get the first post (or handle as you wish)
        print(pos.user_id, pos.category)
    else:
        print("No posts found for this user.")
    return render(request, 'mediaApp/base.html')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # set staff status to True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect("login")
            # return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, "mediaApp/register.html", {"form": form})

@login_required
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def profile_list(request):
    print(request.user.id)
    posts = Post.objects.filter(user = request.user)
    print(posts)
    return render(request, "mediaApp/profilePostList.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(form)
        if form.is_valid():
            print(form)
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            
            return redirect('profile_post')
    else:
        form = PostForm()
    return render(request, 'mediaApp/create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user = request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile_post')
    else:
        form = PostForm(instance=post)
    return render(request, 'mediaApp/create_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user = request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('profile_post')