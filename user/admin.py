from django.contrib import admin
from user.models import Profile, Donate, Role, Achievement, Conviction


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "profile_image",
        "donate",
        "city",
        "social_rating",
    ]
    list_editable = [
        "first_name",
        "profile_image",
        "donate",
        "city",
        "social_rating",
    ]
    search_fields = ["username", "city"]
    list_filter = ["donate__name", "role__name"]
    filter_horizontal = ["achievement", "conviction"]  # Для множественного выбора


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ["name", "responsobility", "image"]
    list_display_links = ["responsobility"]
    list_editable = ["name"]
    ordering = ["-responsobility"]
    search_fields = ["name"]

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "responsobility", "image"]
    list_display_links = ["name"]
    list_editable = ["responsobility"]
    ordering = ["-responsobility"]
    search_fields = ["name"]
    list_filter = ["responsobility"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "earned_date", "image"]
    list_display_links = ["name"]
    list_editable = ["description"]
    ordering = ["-earned_date"]
    search_fields = ["name", "description"]
    list_filter = ["earned_date"]


@admin.register(Conviction)
class ConvictionAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "earned_date", "image"]
    list_display_links = ["name"]
    list_editable = ["description"]
    ordering = ["-earned_date"]
    search_fields = ["name", "description"]
    list_filter = ["earned_date"]