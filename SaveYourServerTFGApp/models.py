import datetime

from django import forms

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone
from django.contrib import admin

from django.db.models.signals import post_save
from django.dispatch import receiver


# --------------------------------------  USER CLASS --------------------------------------

class MyUserManager(BaseUserManager):
    def create_user(self, full_name, dni, email, date_of_birth, password=None):
    #def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address to register')
        
        if not full_name:
            raise ValueError('Users must have a full name to register')	

        if not password:
        	raise ValueError('Users must have a password to register')

        if not dni:
        	raise ValueError('Users must have a dni to register')

        user = self.model(
        	full_name=full_name,
        	dni=dni,
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, full_name, dni, email, date_of_birth, password=None):
    #def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        if not email:
        	raise ValueError('Users must have an email address to register')

        if not full_name:
        	raise ValueError('Users must have a full name to register')	

        if not password:
        	raise ValueError('Users must have a password to register')

        if not dni:
        	raise ValueError('Users must have a dni to register')


        user = self.create_user(
            full_name,
            dni,
            email,
            password=password,
            date_of_birth=date_of_birth,
        )

        user.is_admin = True
        user.is_systemadmin = 0
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        #unique=True,
        blank=True, 
        default="",
    )

    full_name = models.CharField(max_length=255, blank=True, null=True)
    dni = models.CharField(max_length=9, unique = True, default="") 
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_systemadmin = models.IntegerField(null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['date_of_birth', 'full_name', 'email']

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    def get_dni(self):
    	return self.dni

    def get_full_name(self):
    	return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    #@property
    #def is_superstaff(self):
    #    "Is the user a member of superstaff?"
        # Simplest possible answer: All admins are staff
    #    return self.is_superadmin



# --------------------------------------  FILE CLASS --------------------------------------

class File(models.Model):
    #id_file = models.IntegerField(unique=True, null=True)
    #id_file = models.AutoField(primary_key=True, default="")
    upload_date = models.DateTimeField('date uploaded', auto_now_add=True)
    is_malware = models.BooleanField(default=False)
    #file_name = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='', default=True)

    #def __str__ (self):
    #    return self.file_name
    
    @admin.display(
        boolean=True,
        ordering='upload_date',
        description='Uploaded recently?',
    )

    #def get_file_name(self):
    #    return self.file_name
    
    def was_uploaded_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.upload_date <= now

    #@property
    #def id_file(self):
    #    return self.id_file

#class FileForm(forms.ModelForm):

#    def __init__(self, *args, **kwargs):
#        super(FileForm,self).__init__(*args, **kwargs)
#        self.fields['field'].widget.attrs['readonly'] = True

#    class Meta:
#        model = File
#        exclude = ['file_name']        

# --------------------------------------  NOTIFICACION CLASS --------------------------------------

class Notification(models.Model):
    #id_notification = models.IntegerField(unique=True, null=True)
    #id_notification = models.AutoField(primary_key=True, default="")
    
    #upload_date_not = models.DateTimeField('date uploaded', auto_now_add=True)

    upload_date_not = models.DateTimeField(default=timezone.now)
    is_visualized = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    notification_title = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,)

    @receiver(post_save, sender=MyUser)
    def create_welcome_message(sender, **kwargs):
        if kwargs.get('created', False):
            Notification.objects.create(user=kwargs.get('instance'), notification_title="Welcome to the SYS Site!!", message="Thanks for signing up!")

    #@receiver(post_save, sender=MyUser)
    #def create_file_message(sender, **kwargs):
        #if kwargs.get(, False):
            #Notification.objects.create(user=kwargs.get('instance'), notification_title="File Uploaded", message="Your file has been updated, after analyze this file, it hasn't a malware")


    @admin.display(
        boolean=True,
        ordering='upload_date_not',
        description='Uploaded notification recently?',
    )

    def was_uploaded_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.upload_date_not <= now

    #def get_message(self):
    #    return self.message

    #def get_notification_title(self):
    #    return self.notification_title

    #@property
    #def id_notification(self):
    #    return self.id_notification



