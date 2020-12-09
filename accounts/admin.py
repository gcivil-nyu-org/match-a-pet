from django.contrib import admin
from .models import ShelterRegisterData, Pet, UserRegisterData, User, Message
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.site_header = "Math-A-Pet Admin Page"

admin.site.register(Message)


@admin.register(User)
class UserModelAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "city",
        "state",
        "last_login",
        "is_active",
        "is_shelter",
        "is_clientuser",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "email",
        "username",
    )
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    pass


# admin.site.register(ShelterRegisterData, RegisterShelterAdmin)
# admin.site.register(User, UserModelAdmin)
# admin.site.register(UserRegisterData, ClientUserModelAdmin)


@admin.register(Pet)
class PetViewAdmin(ImportExportModelAdmin):
    pass
    list_display = (
        "id",
        "shelterRegisterData",
        "pet_name",
        "pet_breed",
        "pet_age",
        "pet_color",
        "pet_gender",
        "pet_adoption_status",
        "pet_pending_status",
        "pet_profile_image1",
        "shelterRegisterData_id",
    )
    search_fields = (
        "shelterRegisterData",
        "pet_name",
        "pet_breed",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    pass


@admin.register(ShelterRegisterData)
class ShelterModelAdmin(ImportExportModelAdmin):
    list_display = (
        "user",
        "user_id",
        "shelter_profile_image",
    )
    search_fields = (
        "user",
        "user_id",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    pass


@admin.register(UserRegisterData)
class ClientUserModelAdmin(ImportExportModelAdmin):
    list_display = (
        "user",
        "user_id",
        "user_profile_image",
    )
    search_fields = (
        "user",
        "user_id",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    pass
