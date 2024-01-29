from typing import Any
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.forms import Form
from django.http import HttpRequest
from unfold.admin import ModelAdmin, ModelAdminMixin
from users.models import User, Group
from django.contrib.auth.models import Group as _Group
from django.db import models
from django import forms

# Register your models here.
admin.site.unregister(_Group)


# admin.site.register(User)
@admin.register(User)
class UserAdmin(ModelAdmin):
    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            # fields = "__all__"
            fields = ["username", "password", "is_superuser", "is_staff", "is_active", "groups"]
            widgets = {
                "groups": forms.CheckboxSelectMultiple,
            }

        def save(self, commit: bool = True) -> Any:
            # if first time saving the user, hash the password
            if not self.instance.pk:
                self.instance.password = make_password(self.cleaned_data["password"])

            return super().save(commit)

    search_fields = ["username"]
    form = UserForm
    list_display = ["username", "_groups", "is_staff"]

    def _groups(self, obj):
        groups = obj.groups.all()
        return ", ".join([group.name for group in groups])


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    model = Group

    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }


# create groups for Owner, Manager, Employee and Customer
