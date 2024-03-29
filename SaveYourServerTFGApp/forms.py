from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import MyUser
from .models import File
from .models import Notification

class CreateUserForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('full_name', 'dni', 'email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user	

class UserForm(ModelForm):
	class Meta:
		model = MyUser
		fields = ('full_name', 'dni', 'email', 'date_of_birth', 'password')

class FileForm(ModelForm):
    class Meta:
        model = File
        fields = ('file',)

class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = ('notification_title', 'message') 
