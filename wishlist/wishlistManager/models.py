from django.db import models


class Wishlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    privacy_level = models.IntegerField(max_length=1)
    user = models.ForeignKey('auth.User', related_name='wishlists', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    example_link = models.URLField()
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    default = models.BooleanField()
    user = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE)

    def __str__(self):  
        return self.name

class ItemCategory(models.Model):
    item = models.ForeignKey(Item, related_name='item_categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='item_categories', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('item', 'category',)

    def __str__(self):
        return self.item.name + " - " + self.category.name
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='group_members', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='group_members', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'user',)

    def __str__(self):
        return self.group.name + " - " + self.user.username
    
class GroupWishlistPermission(models.Model):
    group = models.ForeignKey(Group, related_name='group_wishlists', on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, related_name='group_wishlists', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('group', 'wishlist',)

    def __str__(self):
        return self.group.name + " - " + self.wishlist.name

class UserWishlistPermission(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_wishlists', on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, related_name='user_wishlists', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'wishlist',)

    def __str__(self):
        return self.user.username + " - " + self.wishlist.name

