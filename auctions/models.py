from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=24)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    item_image = models.ImageField(upload_to='images/', blank=True, null=True)
    item_name = models.CharField(max_length=64)
    item_desc = models.CharField(max_length=128)
    starting_bid = models.FloatField()
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="classified")

    def __str__(self):
        # return f"Item {self.id}: {self.item_name}, {self.item_desc}, {self.starting_bid}, {self.item_category}"
        return f"Item {self.id}: {self.item_name}"

# def get_image_path(instance, filename):
#     return os.path.join('photos', str(instance.id), filename)