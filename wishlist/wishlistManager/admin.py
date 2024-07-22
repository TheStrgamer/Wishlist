from django.contrib import admin

from .models import Wishlist, Category, Item, WishlistGroup, GroupInvite

# Register your models here.

admin.site.register(Wishlist)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(WishlistGroup)
admin.site.register(GroupInvite)
