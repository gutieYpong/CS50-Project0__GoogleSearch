from django.contrib import admin

from .models import User, Listing, Category, Bidder
# from .models import User, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Bidder)