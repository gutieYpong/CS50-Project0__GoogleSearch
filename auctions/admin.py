from django.contrib import admin

from .models import User, Listing, Category
# from .models import User, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Category)
