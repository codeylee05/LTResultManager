from django import forms
from django.contrib.auth.models import User
from .models import Parent

import logging
logger = logging.getLogger(__name__)


class ParentAdminForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Parent
        fields = ['children']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['password'].required = False

    def save(self, commit=True):
        try:
            if self.instance.pk is None:
                logger.warning("Creating a new Parent")
                username = self.cleaned_data.pop('username')
                email = self.cleaned_data.pop('email')
                password = self.cleaned_data.pop('password')

                logger.warning(f"Creating user: {username}, {email}")
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                logger.warning(f"User created: {user}")

                parent = super().save(commit=False)
                parent.user = user
                if commit:
                    parent.save()
                    self.save_m2m()
                return parent
            else:
                logger.warning("Editing existing Parent")
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
        except Exception as e:
            logger.error("Error in ParentAdminForm save():", exc_info=True)
            raise
