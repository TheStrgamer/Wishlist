from django.shortcuts import render, redirect

from .models import Wishlist, Category, Item, WishlistGroup, GroupInvite

from .forms import UserRegisterForm, WishlistForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from django.views import View



# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_wishlist_view(request):
    if request.method== "POST":
        form = WishlistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        
    else: 
        form = WishlistForm()
    context = {'form': form}
    return render(request, 'wishlist/create_wishlist.html', context)

@login_required
def wishlist_view(request):
    wishlists = Wishlist.objects.all()
    wishlists_with_permission = [wishlist for wishlist in wishlists if wishlist.user_can_view(request.user)]
    context = {'wishlist_list': wishlists_with_permission}
    return render(request, 'wishlist/wishlist_overview.html', context)

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
    

class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        return render(request, 'registration/protected.html')





