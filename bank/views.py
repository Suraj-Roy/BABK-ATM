from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Banking import settings
from django.core.mail import send_mail
from random import randint
import uuid
from .models import Profile,ATM
from atm.models import Account


# Create your views here.

def home(request):
    return render(request,'bank/home.html')


def Login(request):
     
    if request.method=='POST':
        
        username = request.POST["email"]
        pass1 = request.POST["password"]

        user = authenticate(username=username,password=pass1)
        if user is not None:
            user_obj = User.objects.filter(username = username).first()

            profile_obj = Profile.objects.filter(user = user_obj ).first()

            if not profile_obj.is_verified:
                messages.error(request, 'Profile is not verified check your mail.')
                return redirect('login')
            
            
            if user is not None:
                login(request,user)
                request.session['name']=user.email
                return redirect('atmpage')
                
        else:
            messages.error(request,"Email or Password is wrong!!!")
            return redirect('login')
    return render(request,'bank/login.html')




def signup(request):
    if request.method=="POST":
        username=request.POST["email"]
        fname = request.POST["fn"]
        lname = request.POST["ln"]
        email = request.POST["email"]
        pass1 = request.POST["password"]
        pass2 = request.POST["password1"]
        

        # if User.objects.filter(username=username):
        #     messages.error(request,"User name already exist")
        #     return redirect('Signin')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email already exist")
            return redirect('signup')

        # if len(username)>10:
        #     messages.error(request,"User name must be under 10 characters")
        #     return redirect('home')

        if pass1 != pass2:
            messages.error(request,"password did not match")
            return redirect('signup') 

        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname

        
        
        myuser.save()
        messages.success(request,"Account created sucessfully")

        

        auth_token = str(uuid.uuid4())
        profile_obj = Profile.objects.create(user=myuser,auth_token=auth_token)
        profile_obj.save()
        
        ATM.objects.create(
            user=myuser,
            name=myuser.email,
            cardno=randint(100000,999999)
            ).save()

        Account(
            user=myuser,
            name=myuser.email
        ).save()

        subject = "welcome to Bank-Login!!!"
        message = "Hello "+myuser.first_name+"!!\n"+"Welcome to virtual Bank/ATM website.\nThank you for visiting our website.\n\n" f'Please click the link to verify http://127.0.0.1:8000/verify/{auth_token}'+"\n\nThanking you\n Suraj Kumar\n"
        
        from_email = settings.EMAIL_HOST_USER
        to_list=[myuser.email]


        send_mail(subject,message,from_email,to_list,fail_silently=True)

        
        return redirect('login')
        



        
    return render(request,'bank/signup.html')


def Logout(request):
    logout(request)
    
    return redirect('home')

def verify(request,token):
    obj=Profile.objects.get(auth_token=token)
    try:
        
        if str(token)==str(obj.auth_token):
            print(str(token)==str(obj.auth_token))

            obj.is_verified=True

            obj.save()
            messages.success(request,'Email verified')
            return redirect('login')

    except Exception as e:
        messages.error(request,'Email not verified verified')
        return redirect('home')

def atmpage(request):
    atm=ATM.objects.filter(name=request.session['name']).first()
    
    # cdn=atm.cardno
    # apn=atm.pinno
    context={'atm':atm}
    return render(request,'bank/atmcard.html',context)

def ChangePassword(request,token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(auth_token = token).first()
        context = {'user_id' : profile_obj.user.id}
        
        if request.method == 'POST':
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')
            user_id = request.POST.get('user_id')
            
            if user_id is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'Password Missmatch.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')
            
            
            
        
        
    except Exception as e:
        print(e)
    return render(request , 'bank/change-password.html' , context)
    



def ForgetPassword(request):
    try:
        if request.method=='POST':
            username = request.POST['email']

            if not User.objects.filter(username=username).first():
                messages.success(request,'No user found with this email.')
                return redirect('forget-password')

            user_obj = User.objects.get(username=username)
            auth_token = str(uuid.uuid4()) 
            profile_obj= Profile.objects.get(user = user_obj)
            profile_obj.auth_token = auth_token
            profile_obj.save()


            subject = "Forgot Password!!!"
            message = "Hello "+user_obj.first_name+"!!\n"+"Welcome to virtual Bank/ATM website.\nThank you for visiting our website.\n\n" f'Please click the ling to reset password.\nhttp://127.0.0.1:8000/change-password/{auth_token}'+"\n\nThanking you\n Suraj Kumar\n"
            
            from_email = settings.EMAIL_HOST_USER
            to_list=[user_obj.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            messages.success(request, 'An email is sent.')
            return redirect('forget-password')

    except:
        pass

    return render(request , 'bank/forget-password.html')



def ChangePin(request):
    context = {}

    try:
        if request.method == 'POST':
            otp = request.POST.get('OTP')
            new_password = request.POST.get('password1')
            confirm_password = request.POST.get('password2')

            user_obj = Account.objects.get(name=request.session['username'])
            
            if user_obj is  None:
                messages.error(request, 'No user id found.')
                return redirect('Change-Pin')
                
            
            if  new_password != confirm_password:
                messages.error(request, 'Pin Missmatch.')
                return redirect('Change-Pin')

            if user_obj.otp != otp:
                messages.error(request, 'OTP Missmatch.')
                return redirect('Change-Pin')

            if len(new_password)!=4:
                messages.error(request, 'Pin must be of 4 digits!!!')
                return redirect('Change-Pin')

            if not new_password.isdigit():
                messages.error(request, 'Please Enter only numbers!!!')
                return redirect('Change-Pin')
            
            user_obj1 = ATM.objects.get(name=request.session['username'])
            user_obj1.pinno=new_password
            user_obj1.save()
            messages.success(request,'pin reset sucessfully!!!')
            return redirect('atm')
            
            
            
        
        
    except Exception as e:
        messages.error(request,'Please valid credentials!!!')
        return redirect('Change-Pin') 
    return render(request , 'bank/change-pin.html' , context)
    



def ForgetPin(request):
    try:
        if request.method=='POST':
            username = request.POST['email']

            if not User.objects.filter(username=username).first():
                messages.success(request,'No user found with this email.')
                return redirect('Forget-Pin')

            user_obj = User.objects.get(username=username)
            request.session['username']=username
            otp = randint(1000,9999)
            account_obj= Account.objects.get(user = user_obj)
            account_obj.otp = str(otp)
            account_obj.save()


            subject = "Forgot Pin/Change Pin!!!"
            message = "Hello "+user_obj.first_name+"!!\n"+"Welcome to virtual Bank/ATM website.\nThank you for visiting our website.\n\n"+ f'Your OTP is : {otp}'+"\n\nThanking you\n Suraj Kumar\n"
            
            from_email = settings.EMAIL_HOST_USER
            to_list=[user_obj.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            messages.success(request, 'An email is sent.')
            return redirect('Change-Pin')

    except:
        pass

    return render(request , 'bank/forget-pin.html')
 