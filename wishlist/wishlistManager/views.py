from django.shortcuts import render

from .models import Wishlist, Category, Item, WishlistGroup, GroupInvite


# Create your views here.

def index(request):
    wishlists = Wishlist.objects.all()
    items = Item.objects.all()
    context = {'wishlists': wishlists}
    return render(request, 'index.html', context)

