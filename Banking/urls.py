"""Banking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bank.views import (home,Login,signup,Logout,
                        verify,atmpage,ChangePassword,
                        ForgetPassword,ChangePin,ForgetPin)
from atm.views import Atm,test,validation,balance,deposit,withdrawl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/',Login,name='login'),
    path('signup/',signup,name='signup'),
    path('logout/',Logout,name='logout'),
    path('verify/<slug:token>',verify,name='verify'),
    path('Mainpage/',atmpage,name='atmpage'),
    path('atm/',Atm,name='atm'),
    path('balance/',balance,name='balance'),
    path('validation/<slug:data>',validation,name='validation'),
    path('validation/',validation,name='validation'),
    path('deposit/<slug:data>',deposit,name='deposit'),
    path('deposit/',deposit,name='deposit'),
    path('withdrawl/',withdrawl,name='withdrawl'),
    path('withdrawl/',withdrawl,name='withdrawl'),
    path('forget-password/' , ForgetPassword , name="forget_password"),
    path('change-password/<slug:token>/' , ChangePassword , name="change-password"),
    path('Forget-Pin/' , ForgetPin , name="Forget-Pin"),
    path('Change-Pin/' , ChangePin , name="Change-Pin"),
    
]
