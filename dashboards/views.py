from django.shortcuts import render, redirect
from blog.models import Category, blogs
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm,BlogPostForm
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .forms import AddUserForm, EditUserForm
# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_counts=Category.objects.all().count()
    blogs_counts= blogs.objects.all().count()
    context={
        'category_counts': category_counts,
        'blogs_counts': blogs_counts
    }
    return render(request,'dashboard.html', context)

def categories(request):
    return render(request, 'categories.html')


def add_categories(request):
    if request.method=="POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm()
    context={
        'form':form
    }
    return render(request, 'add_categories.html',context)
def edit_categories(request,pk):
    category=get_object_or_404(Category, pk=pk)
    if request.method=="POST":
        form=CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form=CategoryForm(instance=category)
    context={
        'form':form,
        'category':category
    }
    
    return render(request, 'edit_categories.html', context)

def delete_categories(request, pk):
    category=get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts=blogs.objects.all()
    context={
        'posts':posts
    }
    return render(request,'posts.html',context)


def add_posts(request):

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            title = form.cleaned_data['title']
            base_slug = slugify(title)
            unique_slug = base_slug
            num = 1
            while post.__class__.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            post.slug = unique_slug
            post.save()
            print("Success")
            return redirect('posts')
        else:
            print("Form errors:", form.errors)
    else:
        form = BlogPostForm()
    context = {'form': form}
    return render(request, 'add_posts.html', context)

def edit_posts(request, pk):
    post = get_object_or_404(blogs, pk=pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            title = form.cleaned_data['title']
            base_slug = slugify(title)
            unique_slug = base_slug
            num = 1

            while blogs.objects.filter(slug=unique_slug).exclude(pk=post.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            post.slug = unique_slug
            post.save()
            return redirect('posts')  
    else:
        form = BlogPostForm(instance=post)
    context = {
        'form': form,
        'post': post
    }
    return render(request, 'edit_posts.html', context)

def delete_posts(request, pk):
    posts=get_object_or_404(blogs, pk=pk)
    posts.delete()
    return redirect('posts')

def users(request):
    users=User.objects.all()
    context={
        'users':users
    }
    return render(request, 'users.html', context)



def add_users(request):
    if request.method=="POST":   
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('users')
    form = AddUserForm()
    context={
        'form':form
    }

    return render(request, 'add_users.html',context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk) 
    if request.method == "POST":
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
    return render(request, 'edit_users.html', context)

def delete_user(request, pk):
    user = get_object_or_404(User,pk=pk)
    user.delete()
    return redirect('users')


  