from .forms import RegistrationForm
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
# from django.contrib.auth import authenticate,logout,login
from django.contrib import messages
from django.http import HttpResponseRedirect
from blog.models import Category, blogs, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

# from django.db.models import Q

# Create your views here.

def register(request):
    if (request.method == "POST"):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context={
        'form':form
    }
    return render(request, 'registerUser.html', context)
   
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  
            if user is not None:
                auth_login(request, user)  
                return redirect('dashboard')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }
    return render(request, 'loginPage.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')
   

def home(request):
    categories= Category.objects.all()
    featured_post =  blogs.objects.filter(is_featured=True,status='published')
    Post = blogs.objects.filter(is_featured=False, status='published')
    # print(featured_post)
    context = {
        'categories': categories,
        'featured_post':featured_post,
        'Post': Post
    }
    return render(request,"home.html", context)

def posts_by_category(request, category_id):
    posts=blogs.objects.filter(status='published',category=category_id)
    try:
        category= Category.objects.get(pk=category_id)
    except:
        return redirect('home')
    # category=get_object_or_404(Category, pk=category_id)
    context={
        'posts':posts,
        'category':category
    }
    return render(request, 'posts_by_category.html',context)

def blogPage(request, slug):
    single_post = get_object_or_404(blogs, slug=slug, status='published')
    if request.method=="POST":
        comment=Comment()
        comment.user = request.user
        comment.Blog=single_post
        comment.comment = request.POST['comment']
        comment.save()
        return HttpResponseRedirect(request.path_info)
    comments = Comment.objects.filter(Blog=single_post)
    comment_count = comments.count()
    print(comments)
    context = {
        'single_post': single_post,
        'comments': comments,
        'comment_count':comment_count
    }
    return render(request,'blogPage.html', context)
def search(request):
    keyword = request.GET.get('keyword')
    blog =blogs.objects.filter(title__icontains=keyword)
    #(Q(title__icontains=keyword)| Q(short_discription_icontains=keyword)|Q(blog_body_icontains=keyword))
    print("value: ",blog)
    content={
        'blog':blog,
        'keyword':keyword
    }
    return render(request, 'search.html', content)