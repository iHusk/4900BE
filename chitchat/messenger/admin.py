from django.contrib import admin
from .models import *

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from messenger.models import Profile

# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['email']

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
        model = Profile
        fields = ('email', 'password', 'phone', 'status', 'type', 'image_id')


class ProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'type')
    list_filter = ('type',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('type',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



class ImageList(admin.ModelAdmin):
    list_display = ['image_path']
    ordering = ['image_path']


class MessageList(admin.ModelAdmin):
    list_display = ('user_id', 'message_contents', 'message_datetime', 'message_type')
    list_filter = ['message_type']
    search_fields = ('user_id', 'message_contents')
    ordering = ('user_id', 'message_datetime')


class ReportList(admin.ModelAdmin):
    list_display = ('user_id', 'report_contents', 'report_datetime', 'message_id')
    search_fields = ('user_id', 'report_contents', 'message_id')
    ordering = ['user_id']


admin.site.register(Image, ImageList)
admin.site.register(Message, MessageList)
admin.site.register(Report, ReportList)
admin.site.register(Profile, ProfileAdmin)