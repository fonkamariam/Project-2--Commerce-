from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class Listing(models.Model):
    title= models.CharField(max_length=64)  
    starting_bid=models.IntegerField()
    description= models.TextField()
    imageUrl= models.CharField(max_length=512 ,blank=True, null=True)
    category=models.TextField(blank=True, null=True)
    owner= models.ForeignKey( User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist= models.ManyToManyField(User, blank=True, null=True, related_name="wl")
    bought= models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True, related_name="bo")
    active=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.id}) {self.title}"