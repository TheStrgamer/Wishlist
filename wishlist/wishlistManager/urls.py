from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

#Define list of urls for the wishlistManager app
urlpatterns = [
    path("", views.index, name="index"),
    path("wishlist/create", views.create_wishlist_view, name="create_wishlist"),
    path("wishlist/", views.wishlist_view, name="wishlist_list"),
    path("wishlist/your_wishlists", views.your_wishlists_view, name="your_wishlists"),
    path('wishlist/<int:wishlist_id>/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/<int:wishlist_id>/add_item', views.add_item_view, name='add_item'),
    path("groups/", views.groups_view, name="groups"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_user_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

