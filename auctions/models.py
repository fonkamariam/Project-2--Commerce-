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
    active=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.id}) {self.title}"
class Watchlist(models.Model):
    own= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="userWL")
    oneauction=models.ManyToManyField(Listing, related_name="oneauction", blank=True, null=True)
    def __str__(self):
        return f"{self.own}'s Listing"  
class Comment(models.Model):
    person=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user1")
    comment=models.TextField()
    auction=models.ForeignKey(Listing ,on_delete=models.CASCADE)
    def __str__(self):
        return f" comment on {self.auction.title} by {self.person}"
class Bid(models.Model):
    bidder= models.ForeignKey( User, on_delete=models.CASCADE)
    bid= models.IntegerField()
    auctionbided=models.ForeignKey( Listing ,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.bidder} bided on {self.auctionbided}"