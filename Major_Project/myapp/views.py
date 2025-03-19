from django.shortcuts import render
from .models import User,Product
from django.core.mail import send_mail
from django.conf import settings
import random


def index(request):
    return render(request,'index.html')
def seller_index(request):
    return render(request,'seller-index.html')
def contact(request):
    return render(request,'contact.html')
def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                request.session['profile_picture']=user.profile_picture.url
                if user.usertype=="buyer":
                    return render(request,'index.html')
                else:
                    return render(request,'seller-index.html')
            else:
                msg="Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email Id Not Registered"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')


def register(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="User Already Registered"
            return render(request,"register.html",{'msg':msg})
        except:
            if request.POST['password']== request.POST['cpassword']:
                User.objects.create (
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                    profile_picture=request.FILES['profile_picture'],
                    usertype=request.POST['usertype'])
                msg="User Register Successfully"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password And Confirm Password Does not Matched"
                return render(request,'register.html',{'msg':msg})

    
    else:
         return render(request,'register.html')
    
def logout(request):
    try:
        del request.session['email'],
        del request.session['fname'],
        del request.session['profile_picture']
        return render(request,"login.html")
    except:
        return render(request,"login.html")
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.email=request.POST['email']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        request.session['profile_picture']=user.profile_picture.url
        msg="Profile Updated Successfully"
        if user.usertype=="buyer":
            return render(request,'profile.html',{'msg':msg, 'user':user})
        else:
            return render(request,'seller-profile.html',{'msg':msg, 'user':user})
    else:
         if user.usertype=="buyer":
             return render(request,'profile.html',{'user':user}) 
         else:
            return render(request,'seller-profile.html',{'user':user})  
def change_password(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        
        if user.password == request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    del request.session['profile_picture']
                    return render (request,'login.html')
                else:
                    msg="Your New Password Can't be from Your old Password"
                    if user.usertype=='buyer':
                        return render(request,'change-password.html',{'msg':msg})
                    else:
                        return render(request,'seller-change-password',{'msg':msg})
            else:
                msg="Your New Password & Confirm Password Does Not Matched"
                if user.usertype=='buyer':
                    return render(request,'change-password.html',{'msg':msg})
                else:
                     return render(request,'seller-change-password',{'msg':msg}) 
        else:
            msg="Old Password Does Not Matched"
            if user.usertype=='buyer':
                return render(request,'change-password.html',{'msg':msg})
            else:
                return render(request,'seller-change-password',{'msg':msg})
    else:  
        if user.usertype=='buyer':
            return render(request,'change-password.html')
        else:
            return render(request,'seller-change-password')
    
def forgot_password(request):
    if request.method=="POST":       
        try:
            user=User.objects.get(email=request.POST['email']) 
            otp =random.randint(1000,9999)
            message="Your OTP for forgot Password is " + str(otp)
            send_mail('OTP For Forgot Password', message, settings.EMAIL_HOST_USER,[user.email,])
            request.session['otp']=otp
            request.session['email']=user.email
            return render(request,'otp-html')
        except Exception as e:
            print(e)
            msg="Email Not Registered"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')

def verify_otp(request):
    if int(request.session['otp'])==int(request.POST['otp']):
        del request.session['otp']
        msg="Create Your New Password"
        return render(request,'new-password.html',{'msg':msg})
    else:
        msg="Invalid OTP"
        return render(request,'otp.html',{'msg':msg})
    
def new_password(request):
    user=User.objects.get(email=request.session['email'])
    if user.password!=request.POST['new_password']:
        if request.POST['new_password']==request.POST['cnew_password']:
            
            user.password=request.POST['new_password']
            user.save()
            msg="Password updated Successfully"
            del request.session['email']
            return render(request,'login.html',{'msg':msg})
        else:
            msg="New Password & Confirm New password Does not Matched"
            return render(request,'new-password.html',{'msg':msg})
    else:
        msg="Old & New Password Can't be same"
        return render(request,'new-password.html',{'msg':msg})

def seller_add_product(request):
    return render(request,'seller-add-product.html')