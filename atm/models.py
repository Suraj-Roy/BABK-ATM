from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    otp= models.CharField(max_length=50,blank=True)
    Account_balance =models.CharField(max_length=500,default=0,blank=True)