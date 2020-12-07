from django.contrib import admin

from .models import User, Listing, Category, Bidder, Comment

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Bidder)
admin.site.register(Comment)