from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Token


# Register your models here.

@admin.register(Token)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ('Token',)
    list_display_links = None
    list_editable = []

    def save_model(self, request, obj, form, change):
        return None

    def change_view(self, request, object_id, **kwargs):
        return None

    def has_add_permission(self, request):
        return None

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return None


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.site_title = "Jsonhub"
admin.site.site_header = "Jsonhub"
