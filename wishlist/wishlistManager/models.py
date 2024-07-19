from django.db import models


class Wishlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    privacy_level = models.IntegerField(max_length=1)
    user = models.ForeignKey('auth.User', related_name='wishlists', on_delete=models.CASCADE)
    groups_with_permission = models.ManyToManyField('Group', related_name='wishlists')
    users_with_permission = models.ManyToManyField('auth.User', related_name='wishlists')

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    default = models.BooleanField()
    user = models.ForeignKey('auth.User', related_name='categories', on_delete=models.CASCADE, null=True)

    def __str__(self):  
        return self.name
    
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    example_link = models.URLField()
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('auth.User', related_name='groups', on_delete=models.CASCADE)
    members = models.ManyToManyField('auth.User', related_name='groups')

    def __str__(self):
        return self.name

    
class GroupInvite(models.Model):
    group = models.ForeignKey(Group, related_name='group_invites', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='group_invites', on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        unique_together = ('group', 'user',)

    def __str__(self):
        return self.group.name + " - " + self.user.username
    


