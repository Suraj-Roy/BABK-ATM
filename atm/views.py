from django.shortcuts import render,redirect
from .models import Account
from django.contrib.auth.models import User
from bank.models import Profile,ATM
from django.contrib import messages
# Create your views here.


def Atm(request):
    return render(request,'atm/atmmainpage.html')

def balance(request):
    balance = Account.objects.get(name=request.session['email'])
    return render(request,'atm/balance.html',{'balance':balance,'fn':balance.user.first_name})

def reset(request):
    pass

def withdrawl(request):
    pass

def deposit(request):
    return render(request,'atm/enteramount.html')

def validation(request,data=None):
    print(data)
    if request.method=='POST':
        cardno = request.POST['atmno']
        pinno=  request.POST['pin']
        print(data)
        try:
            user_detail = ATM.objects.get(cardno=cardno,pinno=pinno)
            if user_detail is not None:
                #request.session['name']=user_detail.name
                
                request.session['email']=user_detail.user.email
                print(request.session['email'])
                print(data)
                return redirect(data)
            messages.error(request,'Wrong Card No. or Pin No.!!!')
            return redirect('validation')
        except:
            messages.error(request,'Wrong Card No. or Pin No.!!!')
            return render(request,'atm/validationform.html',{'data':data})
    return render(request,'atm/validationform.html')

def test(request):
    return render(request,'atm/validationform.html')


def deposit(request,data=None):
    if request.method=='POST':
        bal=Account.objects.get(name=request.session['email'])
        val = request.POST['amount']
        bal.Account_balance=str(int(val)+int(bal.Account_balance))
        messages.success(request,f'Rs.{val} deposited sucessfully.')
        bal.save()
        return redirect('balance')
    return render(request,'atm/enteramount.html')

def withdrawl(request,data=None):
    if request.method=='POST':
        bal=Account.objects.get(name=request.session['email'])
        val = request.POST['amount']
        if int(val)<=int(bal.Account_balance):
            bal.Account_balance=str(int(bal.Account_balance)-int(val))
            messages.success(request,f'Rs.{val} withdrawl sucessfully.')
            bal.save()

            return redirect('balance')
        else:
            messages.error(request,'insufficient amount in account')
            return redirect('withdrawl')
    return render(request,'atm/enteramount.html')

    

