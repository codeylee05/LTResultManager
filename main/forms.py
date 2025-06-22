from django import forms
from .models import Parent
from django.contrib.auth.models import User


class ParentAdminForm(forms.ModelForm):
    # To create a parent with a user account in one go
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Parent
        fields = ['username', 'email', 'password', 'children']

    def save(self, commit=True):
        username = self.cleaned_data.pop('username')
        email = self.cleaned_data.pop('email')
        password = self.cleaned_data.pop('password')

        user = User.objects.create_user(
            username=username, email=email, password=password)

        parent = super().save(commit=False)
        parent.user = user
        if commit:
            parent.save()
            self.save_m2m()
        return parent
