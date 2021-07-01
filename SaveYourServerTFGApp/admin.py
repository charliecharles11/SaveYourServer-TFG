from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.admin import AdminSite
import csv
from django.http import HttpResponse

from django.shortcuts import render, redirect

from .models import MyUser
from .models import File
from .models import Notification

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta) 
        writer = csv.writer(response)
        
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names]) 


        return response

        export_as_csv.short_description = "Export Selected"

class UserCreationForm(forms.ModelForm):
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


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('id', 'full_name', 'dni', 'email', 'password', 'date_of_birth', 'is_admin','is_active')

class UserAdmin(BaseUserAdmin, ExportCsvMixin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'full_name', 'dni', 'email', 'date_of_birth', 'is_admin', 'is_systemadmin', 'is_active')
    list_filter = ('is_admin',  'is_systemadmin', 'is_active')
    actions = ["export_as_csv"]

    fieldsets = (
        (None, {
        	'classes': ('wide',),
        	'fields': ('full_name', 'dni', 'email', 'password')
        }),
        ('Permissions', {'fields': ('is_admin', 'is_systemadmin', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'dni', 'email', 'date_of_birth', 'password1', 'password2'),
        }),
        ('Permissions', {'fields': ('is_admin','is_systemadmin',)}),
    )
    search_fields = ('email','full_name','dni')
    ordering = ('email',)
    filter_horizontal = ()
    
    
# ---------------------------- FILE CLASS ----------------------------
    
class FileAdmin(admin.ModelAdmin, ExportCsvMixin):

    list_display = ('id', 'is_malware', 'file', 'upload_date')
    list_filter = ['upload_date']
    actions = ["export_as_csv"]

    readonly_fields = ('id', 'is_malware', 'file', 'upload_date')

    #fieldsets = [
    #    (None,          {'fields': ['id', 'upload_date', 'file_name',]}),
    #    ('Permissions', {'fields': ['is_malware']}),
    #]


    #add_fieldsets = (
    #    (None, {
    #        'classes': ('wide',),
    #        'fields': ('id', 'upload_date', 'file_name'),

    #     }),
    #)

    search_fields = ('id', 'is_malware',)
    ordering = ('id',)
    filter_horizontal = ()



# ---------------------------- NOTIFICATION CLASS ----------------------------

class NotificationAdmin(admin.ModelAdmin, ExportCsvMixin):

    list_display = ('id', 'is_visualized', 'message', 'notification_title', 'upload_date_not', 'user')
    list_filter = ['upload_date_not']

    readonly_fields = ('id', 'is_visualized', 'message', 'notification_title' , 'upload_date_not','user')

    #fieldsets = [
    #    (None,          {'fields': ['id', 'notification_title',]}),
    #    ('Body of the message', {'fields': ['message']}),
    #]


    #add_fieldsets = (
    #    (None, {
    #        'classes': ('wide',),
    #        'fields': ('id_notification', 'notification_title'),

    #     }),
    #)

    search_fields = ('id',)
    ordering = ('id',)
    filter_horizontal = ()


# -------------------- ADMIN CLASS (ONLY SYSTEM ADMINS) ----------------------

#class SystemAdminSite(AdminSite):
#    site_header = "Save Your Server Admin"
#    site_title = "SYS Portal"
#    index_title = "Welcome to the SYS Resercher Portal for System Admins"


#system_admin_site = SystemAdminSite(name='system_admin')

#try:
#    user = MyUser.objects.get(is_systemadmin = 0)
#    if user:
#        admin.site.register(File, FileAdmin)
#        admin.site.register(MyUser, UserAdmin)
#        admin.site.register(Notification, NotificationAdmin)
#except Exception as e:
#    admin.site.register(File, FileAdmin)
#    admin.site.register(Notification, NotificationAdmin)

admin.site.register(File, FileAdmin)
admin.site.register(MyUser, UserAdmin)
admin.site.register(Notification, NotificationAdmin)    

#system_admin_site.register(File, FileAdmin)
#system_admin_site.register(Notification, NotificationAdmin)

admin.site.unregister(Group)
