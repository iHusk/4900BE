from ast import Mod
from pyexpat.errors import messages
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )

        user.save(using=self._db)
        return user


class Image(models.Model):
    image_path = models.ImageField()


class Profile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=254,
        unique=True
    )
    phone = models.CharField(max_length=10,)
    status = models.BooleanField(default=True)
    type = models.CharField(max_length=35, default='user')
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    
    def __str__(self):
        return self.email

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
        return True




class Message(models.Model):
    message_contents = models.CharField(max_length=1000)
    message_datetime = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=10)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Report(models.Model):
    report_contents = models.CharField(max_length=1000)
    report_datetime = models.DateTimeField(auto_now_add=True)
    report_update_datetime = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message_id = models.ForeignKey(Message, on_delete=models.PROTECT)
