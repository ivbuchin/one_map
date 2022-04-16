from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "age", "get_avatar", "is_active",)
    list_display_links = ("username",)
    list_filter = ("is_active",)
    search_fields = ("username",)
    list_editable = ("is_active",)
    readonly_fields = ("get_avatar",)

    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src={obj.avatar.url} width="15" height="15"')

    get_avatar.short_description = "Изображение аватара"

    fieldsets = (
        (None, {
            "fields": (("username", "email"), "age", "master",)
        }),
        (None, {
            "fields": (("about_us", "status"), ("avatar", "get_avatar"),)
        }),
    )
