from django.contrib import admin
from django.db import models
from store.models import Category, Product, ProductImage
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from django.utils.safestring import mark_safe
from django import forms


# Register your models here.


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "safe_description"]
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}

    @admin.display(description="Description")
    def safe_description(self, obj):
        return mark_safe(f"{obj.description[:50]}...")


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    class ImageInline(admin.TabularInline):
        model = ProductImage
        fields = ["image"]
        extra = 1

    class ProductAdminForm(forms.ModelForm):
        # description = forms.CharField(widget=WysiwygWidget)
        class Meta:
            model = Product
            fields = "__all__"
            widgets = {
                "description": WysiwygWidget,
            }

    list_display = ["name", "safe_description", "category", "safe_tags", "safe_images", "base_price", "stock"]
    list_editable = ["base_price", "stock"]
    fields = ["name", "description", "category", "tags", "base_price", "stock"]
    inlines = [ImageInline]
    form = ProductAdminForm

    @admin.display(description="Description")
    def safe_description(self, obj):
        # mark the description as safe then truncate it to 50 characters and add an ellipsis
        return mark_safe(f"{obj.description[:50]}...")

    @admin.display(description="Tags")
    def safe_tags(self, obj):
        tag_string: str = obj.tags
        tags = tag_string.splitlines()[:3]
        tag_display = ""
        for tag in tags:
            tag_display += f"<span style='border-radius:999px; background:darkgray; color:black; padding:5px; margin:2px'>{tag}</span>"
        num_remaining = len(tag_string.splitlines()) - 3
        if num_remaining > 0:
            tag_display += f"<span>+{num_remaining} more</span>"
        return mark_safe(tag_display)

    @admin.display(description="Images")
    def safe_images(self, obj: Product):
        images = obj.images.all()
        # display the first image and add a +n images label if there are more
        image_display = (
            f"<img src='{images[0].image.url}' alt='{images[0].image.name}' width='50' class='product-image'>"
        )
        if len(images) > 1:
            image_display += f"<span>+{len(images) - 1} more</span>"

        image_display = f"<div style='display:flex; align-items:center; gap: 2px;'>{image_display}</div>"

        return mark_safe(image_display)
