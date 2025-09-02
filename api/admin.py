from django.utils.html import format_html
from django.contrib import admin
from .models import DogImage

@admin.register(DogImage)
class DogImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "predicted_breed", "uploaded_at", "image_preview")
    list_filter = ("predicted_breed", "uploaded_at")
    search_fields = ("user__username", "predicted_breed")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image Preview"