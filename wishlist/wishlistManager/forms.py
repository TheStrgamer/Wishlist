from django import forms
from django.contrib.auth.models import User
from .models import WishlistGroup, Wishlist


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    passwordConfirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
    #TODO write more

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
    privacy_level = forms.MultipleChoiceField(choices=[(0, 'Public'), (1, 'Selective'), (2, 'Private')], required=True, label='Privacy Level')
    groups_with_permission = forms.ModelMultipleChoiceField(queryset=WishlistGroup.objects.all(), required=False, label = 'Share with Groups')
    users_with_permission = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, label = 'Share with Users')

    def save(self):
        print('creating' + self.cleaned_data['name'])
    

class WishlistForm2(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['name', 'description', 'privacy_level', 'groups_with_permission', 'users_with_permission']
        widgets = {
            'description': forms.Textarea(),
        }
        labels = {
            'name': 'Wishlist Name',
            'description': 'Description',
            'privacy_level': 'Privacy Level',
            'groups_with_permission': 'Share with Groups',
            'users_with_permission': 'Share with Users',
        }
