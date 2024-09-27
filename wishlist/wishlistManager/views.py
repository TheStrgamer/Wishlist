from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Wishlist, Category, Item, WishlistGroup, GroupInvite

from .forms import UserRegisterForm, WishlistForm, ItemForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.views import View

#user related views

def register_user_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context )


def login_view(request):
    error_message = None 

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'  
            return redirect(next_url)
        else:
            error_message = 'Invalid credentials'
    return render(request, 'accounts/login.html', {'error_message': error_message})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('index')
    else:
        return redirect('index')
    


# Home.
def index(request):
    return render(request, 'index.html')


# Wishlist related views
@login_required
def create_wishlist_view(request):
    if request.method== "POST":
        form = WishlistForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('your_wishlists') 
        else:
            print(form.errors)       
    else: 
        form = WishlistForm(user=request.user)
    context = {'form': form}
    return render(request, 'wishlist/create_wishlist.html', context)

@login_required
def edit_wishlist_view(request, wishlist_id):
    wishlist=get_object_or_404(Wishlist, id=wishlist_id)
    if wishlist.user_is_creator(request.user) == False:
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url) 

    if request.method == "POST":
        form = WishlistForm(request.POST, user = request.user, instance=wishlist)
        if form.is_valid():
            form.save()
            url = reverse('wishlist_detail', args=[wishlist_id])
            return redirect(url) 
    else:
        form = WishlistForm(user = request.user, instance=wishlist)
    context = {'form':form}
    return render(request, 'wishlist/create_wishlist.html', context)

@login_required
def delete_wishlist_view(request, wishlist_id):
    wishlist=get_object_or_404(Wishlist, id=wishlist_id)
    if wishlist.user_is_creator(request.user) == False:
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url) 
    if request.method == "POST":
        wishlist.delete()
        return redirect('your_wishlists')
    context = {'name': wishlist.name, 'type': 'wishlist', 'wishlist':wishlist}
    return render(request, 'confirm_delete.html', context)


    

@login_required
def add_item_view(request, wishlist_id):
    wishlist=get_object_or_404(Wishlist, id=wishlist_id)
    if wishlist.user_is_creator(request.user) == False:
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url) 
    #wishlist = Wishlist.objects.filter(id = wishlist_id)
    if request.method== "POST":
        form = ItemForm(request.POST, request.FILES, user=request.user, wishlist = wishlist )
        if form.is_valid():
            form.save()

            url = reverse('wishlist_detail', args=[wishlist_id])
            return redirect(url) 
        else:
            print(form.errors)       
    else: 
        form = ItemForm(user=request.user, wishlist = wishlist)
    context = {'form': form}
    return render(request, 'wishlist/add_item.html', context)

@login_required
def edit_item_view(request, item_id, wishlist_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)

    if item.wishlist.user_is_creator(request.user) == False:
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url) 
    
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, user=request.user, wishlist = wishlist, instance=item )
        if form.is_valid():
            form.save()
            url = reverse('wishlist_detail', args=[wishlist_id])
            return redirect(url) 
    else:
        form = ItemForm(user=request.user, wishlist = wishlist, instance=item )
    context = {'form':form}
    return render(request, 'wishlist/add_item.html', context)
    
@login_required
def delete_item_view(request, item_id, wishlist_id):
    item = get_object_or_404(Item, id=item_id)
    wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    if item.wishlist.user_is_creator(request.user) == False:
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url) 

    if request.method == "POST":
        item.delete()
        url = reverse('wishlist_detail', args=[wishlist_id])
        return redirect(url)     
    context = {'name': item.name, 'type': 'item', 'item':item, 'wishlist':wishlist}
    return render(request, 'confirm_delete.html', context)
    




@login_required
def wishlist_view(request):
    wishlists = Wishlist.objects.all()
    wishlists_with_permission = [wishlist for wishlist in wishlists if wishlist.shared_with_user(request.user)]
    context = {'wishlist_list': wishlists_with_permission}
    return render(request, 'wishlist/wishlist_overview.html', context)

@login_required
def your_wishlists_view(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_list': wishlists}
    return render(request, 'wishlist/your_wishlists.html', context)

def wishlist_detail(request, wishlist_id):

    current_wishlist = get_object_or_404(Wishlist, id=wishlist_id)
    items = Item.objects.filter(wishlist = current_wishlist)
    can_view = current_wishlist.user_can_view(request.user)
    if can_view == False:
        # current_wishlist = Wishlist.objects.filter(id = wishlist_id)

        current_wishlist = None
        items = None
    context = {'wishlist': current_wishlist, 'items': items, 'can_view':can_view}
    return render(request, 'wishlist/wishlist.html', context)


# Group related views
@login_required
def groups_view(request):
    groups = WishlistGroup.objects.all()
    your_groups = [group for group in groups if request.user in group.members.all() and group.owner != request.user]
    owned_groups = [group for group in groups if group.owner == request.user]
    context = {'group_list': your_groups, 'owned_groups': owned_groups}
    return render(request, 'groups/groups.html', context)

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(WishlistGroup, id=group_id)
    users = group.members.all()
    owner = group.owner
    can_view = group.can_view(request.user)
    if can_view == False:
        group = None

    wishlists = Wishlist.objects.all()
    wishlists_for_group = [wishlist for wishlist in wishlists if group in wishlist.groups_with_permission.all()]
    context = {'group':group, 'wishlists':wishlists_for_group, 'can_view':can_view, 'users':users, 'owner':owner}
    return render(request, 'groups/group_detail.html', context)
    


class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')





