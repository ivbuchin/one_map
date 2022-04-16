from django.contrib import admin

from .models import Section, Topic, Message


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "section", "author", "views",)
    list_display_links = ("title",)
    list_filter = ("section",)
    search_fields = ("title",)

    fieldsets = (
        (None, {
            "fields": (("title", "url"), "section", "author",)
        }),
        (None, {
            "fields": ("text",)
        }),
    )


@admin.register(Message)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "author", "datetime",)
    list_display_links = ("id",)
    list_filter = ("topic",)
    search_fields = ("text",)
