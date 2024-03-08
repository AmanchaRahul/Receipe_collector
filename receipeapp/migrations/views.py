from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url="/receipepage/")
def receipes(request):
    if request.method=="POST":
        data=request.POST
        receipe_image=request.FILES.get("receipe_image")
        receipe_name=data.get("receipe_name")
        receipe_description=data.get("receipe_description")
        
        
        Receipe.objects.create(
         receipe_image=receipe_image,
         receipe_description=receipe_description,
         receipe_name=receipe_name,
         
        ) 
        
        
        return redirect("/receipepage/")
    
    queryset=Receipe.objects.all()
    context={"receipes":queryset}
    return render(request,"receipes.html",context)
    
   

def delete_receipe(request,id):
    
    queryset=Receipe.objects.get(id=id)
    queryset.delete()
    
    return redirect("/receipepage/")

def update_receipe(request,id):
    
    queryset=Receipe.objects.get(id=id)
    if request.method=="POST":
        data=request.POST
        receipe_image=request.FILES.get("receipe_image")
        receipe_description=data.get("receipe_description")
        receipe_name=data.get("receipe_name")
        
        queryset.receipe_name=receipe_name
        queryset.receipe_description=receipe_description
        
        
        if receipe_image:
            queryset.receipe_image=receipe_image
            
        queryset.save()   
        
        return redirect("/receipepage/")
    
    
    context={
        'receipe':queryset
         }
    
    return render(request,"update_receipes.html",context)



def login_page(request):
    if request.method=="POST":
       
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        print(username)
        print(password)
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid User!")
            return redirect("/loginpage/")
        
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,"Invalid Password!")
            return redirect("/loginpage/")
        
        else:
            
            login(request,user)
            
            return redirect("/receipepage/")
            
        
    return render(request,"login.html")


def logout_page(request):
    logout(request)
    return redirect("/loginpage/")


def register(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user=User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request,"Username already exists!")
            return redirect("/registerpage/")
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
         ) 
        print(first_name)
        print(last_name)
        print(username)
        print(password)
        
        user.set_password(password)
        user.save()
        
        messages.info(request,"Account Created Successfully!")
        
          
        return redirect("/registerpage/")
    
    
    return render(request,"register.html")
   