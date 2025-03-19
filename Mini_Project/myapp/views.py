from django.shortcuts import render
from .models import Contact,User
from django.core.mail import send_mail
from django.conf import settings
import random

def index(request):
    return render(request,'index.html')
def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks'],
        )
        msg="Contact saved successfully"
        contacts=Contact.objects.all().order_by("-id")[:3]
        return render(request,'contact.html',{'msg':msg,'contacts':contacts})
        
    else:
        contacts=Contact.objects.all().order_by("-id")[:3]
        return render(request,'contact.html',{'contacts':contacts})
    
def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = "Email Already Registered"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cfnpassword']:
                User.objects.create(
                    fname  = request.POST['fname'],
                    lname  = request.POST['lname'],            
                    email  = request.POST['email'],
                    mobile  = request.POST['mobile'],
                    address  = request.POST['address'],
                    password  = request.POST['password'],
                    profile_picture=request.FILES['profile_picture']
                )
                msg=" User Sign up Successfully"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does not matched"
                return render(request,'signup.html',{'msg':msg})
    else:    
        return render(request,'signup.html')
def login(request):
    if request.method =="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['name']=user.fname + user.lname
                request.session['email']=user.email
                request.session['profile_picture']=user.profile_picture.url
                return render(request,'index.html')
            else:
                msg = "Incorrect Password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email not registerd"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')
def logout(request):
    try:
       del request.session['email']
       del request.session['name']
       del request.session['profile_picture']
       msg= "User Logged out Successfully "
       return render(request,'login.html',{'msg':msg})
    except:
        return render(request,'login.html')
    
def change_password(request):
    if request.method == "POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password != request.POST['new_password']:
                    user.password=request.POST['new_password']
                    user.save()
                    msg="Password Changed Successfully"
                    del request.session['email']
                    del request.session['name']
                    return render(request,'login.html',{'msg':msg})
                else:
                    msg="Old & New Password Can't be same"
                    return render(request,'change-password.html',{'msg':msg})
            else:
                msg="New password & Confirm New Password does not matched"
                return render(request,'change-password.html',{'msg':msg})
        else:
            msg="Old Password Does Not Matched"
            return render(request,'change-password.html',{'msg':msg})
    else:
        return render(request,'change-password.html')

def forgot_password(request):
    if request.method== "POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            message="Your OTP for Forgot Password is " + str(otp)
            send_mail('OTP For Forgot Password', message, settings.EMAIL_HOST_USER,[user.email,])
            request.session['email']=user.email
            request.session['otp']=otp
            return render(request,'otp.html')
        except:
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
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(email=request.session['email'])
        user.password=request.POST['new_password']
        user.save()
        msg="Password updated Successfully"
        del request.session['email']
        return render(request,'login.html',{'msg':msg})
    else:
        msg="New Password & Confirm New password Does not Matched"
        return render(request,'new-password.html',{'msg':msg})
    
def profile(request):
    user= User.objects.get(email=request.session['email'])
    if request.method=="POST":       
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        try:
            user.profile_picture=request.FILES['profile_picture']
        except:
            pass
        user.save()
        request.session['profile_picture']=user.profile_picture.url
        msg="Profile Updated Successfully"
        return render(request,'profile.html',{'msg':msg})
    else:
        
        return render(request,'profile.html',{'user':user})
    