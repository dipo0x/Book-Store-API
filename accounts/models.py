from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=200)
    country = models.CharField(max_length=50, blank=False) 
    #if by any means y'll create a form to edit profile, dont make them edit this field   
    book = models.IntegerField(default=0, blank=True)    

    def __str__(self):
        return self.name