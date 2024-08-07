from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

#Define list of urls for the wishlistManager app
urlpatterns = [
    path("", views.index, name="index"),

    path("login/", views.login_view, name="login"),
    path("register/", views.register_user_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

spesific_item_patterns = [
    path('edit', views.edit_item_view, name='edit_item'),
    path('delete', views.delete_item_view, name='delete_item'),



]

spesific_wishlist_patterns = [
    path('', views.wishlist_detail, name='wishlist_detail'),
    path('edit', views.edit_wishlist_view, name='edit_wishlist'),
    path('add_item', views.add_item_view, name='add_item'),
    path('delete/', views.delete_wishlist_view, name='delete_wishlist'),
    path('<int:item_id>/', include(spesific_item_patterns)),
]

wishlist_url_patterns = [    
    path("create", views.create_wishlist_view, name="create_wishlist"),
    path("", views.wishlist_view, name="wishlist_list"),
    path("your_wishlists", views.your_wishlists_view, name="your_wishlists"),
    path('<int:wishlist_id>/', include(spesific_wishlist_patterns)),
]


spesific_group_patterns = [
    path("", views.group_detail, name="group_detail")

]

group_url_patterns = [
    path("", views.groups_view, name="groups"),
    path('<int:group_id>/', include(spesific_group_patterns)),


]

urlpatterns += [
    path('wishlist/', include(wishlist_url_patterns)),
    path("groups/", include(group_url_patterns)),
]


