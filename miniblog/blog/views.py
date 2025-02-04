from django.shortcuts import render , HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .forms import signUpForm , LoginForm , PostForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request , 'home.html', {'post':posts})


def about(request):
    return render(request , 'about.html')

def contact(request):
    return render(request , 'contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request , 'dashboard.html', {'posts':post, 'full_name':full_name , 'groups':gps})
    else:
        return HttpResponseRedirect('/userlogin/')


def user_signup(request):
    if request.method == 'POST':
        fm = signUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Congratulations !! You have become an Author.')
            user = fm.save()
            group = Group.objects.get(name="Author")
            user.groups.add(group)
    else:
        fm = signUpForm()
    return render(request , 'signup.html' , {'form':fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request=request , data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(request , username=uname , password=upass)
                if user is not None:
                    login(request , user)
                    messages.success(request , 'Logged in Successfuly !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = LoginForm()
        return render(request , 'login.html' , {'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')
    

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            fm = PostForm()
        return render(request , 'addpost.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')
    
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form':form}) 
    else:
        return HttpResponseRedirect('/login/')
        
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')