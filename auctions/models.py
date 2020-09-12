from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=64, blank=False)

    def __str__(self):
        return self.name


class AuctionListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product")
    title = models.CharField(max_length=128, blank=False)
    description = models.TextField(max_length=9999, blank=False)
    price = models.FloatField(blank=False, default=0.0, max_length=32)
    photo = models.URLField()
    post_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_bid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class Bid(models.Model):
    bid_price = models.FloatField(blank=False, default=0.0, max_length=32)
    bid_count = models.PositiveIntegerField()
    of_product = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.bid_price)


class Comment(models.Model):
    post_comment = models.CharField(max_length=999, blank=True)
    of_product = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.post_comment


class Watchlist(models.Model):
    product = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    watcher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)

        
class WinnerList(models.Model):
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    won_product = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    latest_bid = models.FloatField()

    def __str__(self):
        return str(self.winner.username)