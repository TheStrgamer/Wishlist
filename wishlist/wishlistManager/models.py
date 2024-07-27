from django.db import models
import datetime

class WishlistGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='owned_groups', on_delete=models.CASCADE)
    members = models.ManyToManyField('auth.User', related_name='wishlist_groups')

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    privacy_level = models.IntegerField(default=0)
    user = models.ForeignKey('auth.User', related_name='created_wishlists', on_delete=models.CASCADE)
    groups_with_permission = models.ManyToManyField(WishlistGroup, related_name='wishlists', blank=True, null=True)
    users_with_permission = models.ManyToManyField('auth.User', related_name='wishlists', blank=True, null=True)

    def __str__(self):
        return self.name
    
    def user_is_creator(self, user):
        return self.user == user
    
    def shared_with_user(self, user):

        if self.privacy_level == 1:
            if user in self.users_with_permission.all():
                return True
            for group in self.groups_with_permission.all():
                if user in group.members.all():
                    return True
        return False
    
    def user_can_view(self, user):
        if self.privacy_level == 0:
            return True
        else:
            return self.user_has_permission(user)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    default = models.BooleanField()
    user = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):  
        return self.name
    
    class Meta:
        verbose_name_plural = "categories"
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    example_link = models.URLField(blank=True, null=True)
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
    

    
class GroupInvite(models.Model):
    group = models.ForeignKey(WishlistGroup, related_name='group_invites', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='group_invites', on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        unique_together = ('group', 'user',)

    def __str__(self):
        return self.group.name + " - " + self.user.username
    


