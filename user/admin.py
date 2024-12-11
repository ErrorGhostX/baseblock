from django.contrib import admin
from user.models import Profile, Donate


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "profile_image", "donate", "city", "social_rating"]
    list_editable = ["first_name", "profile_image", "donate", "city", "social_rating"]
    search_fields = ["username", "city"]
    list_filter = ["donate__name"]


@admin.register(Donate)
class DonateAdmin(admin.ModelAdmin):
    list_display = ["name", "responsobility", "image"]
    list_display_links = ["responsobility"]
    list_editable = ["name"]
    ordering = ["-responsobility"]
    search_fields = ["name"]
