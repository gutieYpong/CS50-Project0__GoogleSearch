from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=24)
    cate_image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.id}, {self.category}"


class Listing(models.Model):
    item_image = models.ImageField(upload_to='images/', blank=True, null=True)
    item_name = models.CharField(max_length=64)
    item_desc = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="classified")
    watchlist = models.ManyToManyField(User, blank=True, related_name="favorites")
    bid_count = models.IntegerField(default=0, blank=False)
    is_active = models.BooleanField(default=True)
    item_creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creater")


    def __str__(self):
        return f"Item {self.id}: {self.item_name}"


class Bidder(models.Model):
    bidder_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidderitem")
    bid_count = models.IntegerField()
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="biddername")
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The bidder of item {self.bidder_item} is {self.bidder_name}."


class Comment(models.Model):
    comment_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentitem")
    comment_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentname")
    comment_content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment_content, self.comment_name)

