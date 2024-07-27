from django import forms
from django.contrib.auth.models import User
from .models import WishlistGroup, Wishlist


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
    groups_with_permission = forms.ModelMultipleChoiceField(queryset=WishlistGroup.objects.all(), required=False, label = 'Share with Groups', widget=forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkboxes'}))
    users_with_permission = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False, label = 'Share with Users', widget=forms.CheckboxSelectMultiple(attrs={'class': 'scrollable-checkboxes'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.fields['groups_with_permission'].queryset = WishlistGroup.objects.filter(members=self.user)
        self.fields['users_with_permission'].queryset = User.objects.exclude(pk=self.user.pk)

    def save(self):
        wishlist = Wishlist.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'], privacy_level =self.cleaned_data['privacy_level'], user=self.user)
        wishlist.groups_with_permission.set(self.cleaned_data['groups_with_permission'])
        wishlist.users_with_permission.set(self.cleaned_data['users_with_permission'])
        wishlist.save()
    

