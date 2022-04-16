from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Branch, Lesson, Comment


class LessonAdminForm(forms.ModelForm):
    content = forms.CharField(label="Контент", widget=CKEditorUploadingWidget())

    class Meta:
        model = Lesson
        fields = '__all__'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url", "draft", "get_image", "branch",)
    list_display_links = ("title",)
    list_filter = ("branch",)
    search_fields = ("title",)
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = LessonAdminForm
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="15" height="15"')

    get_image.short_description = "Изображение"

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    fieldsets = (
        (None, {
            "fields": (("title", "url"), "branch", "authors",)
        }),
        (None, {
            "fields": ("description", "content", "task", ("image", "get_image"))
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "lesson", "id",)
    readonly_fields = ("name", "email",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)
