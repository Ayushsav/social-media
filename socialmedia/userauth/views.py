from  django . shortcuts  import  render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import LikePost, Post, Profile



def signup(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        return redirect('/loginn')
    
    return render(request, 'signup.html')
        
     
        
        
        
        
    

def loginn(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        else:
            return redirect('/loginn')
               
    return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')

@login_required(login_url='/loginn')
def home(request):
    post=Post.objects.all().order_by('-created_at')
    return render(request, 'main.html',{'post':post})
    



def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')


def likes(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    

def explore(request):
    post=Post.objects.all().order_by('-created_at')
    return render(request, 'explore.html',{'post':post})

def profile(request):
    profile=Profile.objects.all()
    # post=Post.objects.all().order_by('-created_at')
    post= Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html',{'post':post ,'profile':profile})