from django import forms
from django.contrib.auth.models import User
from .models import Parent


class ParentAdminForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Parent
        fields = ['children']  # Only fields from Parent model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            # Editing existing Parent: pre-fill User fields
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            # Don't prefill password for security reasons
            self.fields['password'].required = False

    def save(self, commit=True):
        if self.instance.pk is None:
            # Creating a new Parent and User
            username = self.cleaned_data.pop('username')
            email = self.cleaned_data.pop('email')
            password = self.cleaned_data.pop('password')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            parent = super().save(commit=False)
            parent.user = user

            if commit:
                parent.save()
                self.save_m2m()
            return parent

        else:
            # Editing existing Parent and User
            parent = super().save(commit=False)
            user = parent.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()

            if commit:
                parent.save()
                self.save_m2m()
            return parent
