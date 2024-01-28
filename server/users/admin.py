from django.contrib import admin
from unfold.admin import ModelAdmin
from users.models import User, Group
from django.contrib.auth.models import Group as _Group

# Register your models here.
admin.site.unregister(_Group)


# admin.site.register(User)
@admin.register(User)
class UserAdmin(ModelAdmin):
    search_fields = ["username"]
    list_display = ["username", "is_staff"]
    pass


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    model = Group
