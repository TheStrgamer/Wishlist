from django.urls import path
from . import views

#Define list of urls for the wishlistManager app
urlpatterns = [
    path("", views.index, name="index"),
]
