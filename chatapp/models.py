from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Registration(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='profile_pic',null=True,blank=True)
  
class Room(models.Model):
    name=models.CharField(max_length=1000)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='receiver')
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
  