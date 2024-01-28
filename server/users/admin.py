from typing import Any
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.forms import Form
from django.http import HttpRequest
from unfold.admin import ModelAdmin
from users.models import User, Group
from django.contrib.auth.models import Group as _Group
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django import forms

# Register your models here.
admin.site.unregister(_Group)


# admin.site.register(User)
@admin.register(User)
class UserAdmin(ModelAdmin):
    search_fields = ["username"]
    list_display = ["username", "is_staff"]
    # fields = ["username", "password", "groups", "superuser_status", ]

    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }

    def save_model(self, request: HttpRequest, obj: User, form: Form, change: Any) -> None:
        user = form.save(commit=False)  # type: ignore
        user.password = make_password(form.cleaned_data["password"])
        user.save()
        # return super().save_model(request, obj, form, change)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    model = Group

    formfield_overrides = {
        models.ManyToManyField: {"widget": forms.CheckboxSelectMultiple},
    }


# create groups for Owner, Manager, Employee and Customer
