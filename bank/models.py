from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    ceated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class ATM(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,blank=True)
    cardno=models.CharField(max_length=6)
    pinno = models.CharField(max_length=4,default='1234')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
