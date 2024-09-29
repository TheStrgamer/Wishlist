from django import forms
from django.contrib.auth.models import User
from .models import WishlistGroup, Wishlist, Category, Item, GroupInvite


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'password', 'passwordConfirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        passwordConfirm = cleaned_data.get('passwordConfirm')
        if password != passwordConfirm and password and passwordConfirm:
            raise forms.ValidationError('Passwords do not match')
        else:
            return cleaned_data


class WishlistForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Wishlist Name')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea)
    privacy_level = forms.ChoiceField(choices=[(0, 'Public'), (1, 'Selective'), (2, 'Private')], required=True, label='Privacy Level', widget=forms.RadioSelect)
    groups_with_permission = forms.ModelMultipleChoiceField(queryset=WishlistGroup.objects.all(), required=False, label = 'Share with Groups', widget=forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkboxes'}))
    users_with_permission = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, label = 'Share with Users', widget=forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkboxes'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.instance = kwargs.pop('instance', None)
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.fields['groups_with_permission'].queryset = WishlistGroup.objects.filter(owner=self.user) | WishlistGroup.objects.filter(members=self.user)
        self.fields['groups_with_permission'].queryset = self.fields['groups_with_permission'].queryset.distinct()
        self.fields['users_with_permission'].queryset = User.objects.exclude(pk=self.user.pk)

        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
            self.fields['privacy_level'].initial = self.instance.privacy_level
            self.fields['groups_with_permission'].initial = self.instance.groups_with_permission.all()
            self.fields['users_with_permission'].initial = self.instance.users_with_permission.all()

    def save(self):
        if self.instance:
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data['description']
            self.instance.privacy_level = self.cleaned_data['privacy_level']
            self.instance.groups_with_permission.set(self.cleaned_data['groups_with_permission'])
            self.instance.users_with_permission.set(self.cleaned_data['users_with_permission'])
        else:
            self.instance = Wishlist.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], privacy_level =self.cleaned_data['privacy_level'], user=self.user)
        self.instance.groups_with_permission.set(self.cleaned_data['groups_with_permission'])
        self.instance.users_with_permission.set(self.cleaned_data['users_with_permission'])
        self.instance.save()
        return self.instance




class ItemForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Item name")
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea)
    link = forms.CharField(max_length=100, required=False, label="Example link ")
    image = forms.ImageField(required=False)
    category = forms.ModelChoiceField(None, required=False, label = 'Category', widget=forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkboxes'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.wishlist = kwargs.pop('wishlist')
        self.instance = kwargs.pop('instance', None)
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(pk=self.user.pk)

        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
            self.fields['link'].initial = self.instance.example_link
            self.fields['image'].initial = self.instance.image 
            self.fields['category'].initial = self.instance.category

    def save(self):
        if self.instance:
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data['description']
            self.instance.example_link= self.cleaned_data['link']
            self.instance.image=self.cleaned_data['image'] 
        else:
            self.instance = Item.objects.create(name = self.cleaned_data['name'], description = self.cleaned_data['description'], example_link= self.cleaned_data['link'], image=self.cleaned_data['image'], wishlist = self.wishlist)
        self.instance.category = (self.cleaned_data['category'])
        self.instance.save()


class WishlistGroupForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Name')
    description = forms.CharField(required=False, label='Description', widget=forms.Textarea)
    image = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        self.instance = kwargs.pop('instance', None)
        super(WishlistGroupForm, self).__init__(*args, **kwargs)


        if self.instance:
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
            self.fields['image'].initial = self.instance.image

    def save(self):
        if self.instance:
            self.instance.name = self.cleaned_data['name']
            self.instance.description = self.cleaned_data['description']
            self.instance.image = self.cleaned_data['image']
        else:
            self.instance = WishlistGroup.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], image = self.cleaned_data['image'], owner=self.owner)
        self.instance.save()
        return self.instance
    
class GroupInviteForm(forms.Form):
    message = forms.CharField(required=False, label='Message')

    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.group = kwargs.pop('group', None)
        self.message = kwargs.pop('message', None)
        super(GroupInviteForm, self).__init__(*args, **kwargs)
        if self.message:
            self.fields['message'].initial = self.message
        
    def save(self):
        if self.group:
            group = self.group
        else:
            group = self.cleaned_data['group']
        if self.message:
            message = self.message
        else:
            message = self.cleaned_data['message']
        try:
            user = self.user
        except User.DoesNotExist:
            return None
        return GroupInvite.objects.create(group=group, user=user, message=message)


