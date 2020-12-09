import django_filters
from django import forms
from .models import Pet, User


class PetFilter(django_filters.FilterSet):

    color_choices = (("Black", "Black"), ("White", "White"))
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    pet_color = django_filters.ChoiceFilter(choices=color_choices)
    pet_gender = django_filters.ChoiceFilter(choices=gender_choices)
    pet_name = django_filters.CharFilter(lookup_expr="icontains")
    pet_breed = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Pet
        fields = ("pet_name", "pet_breed", "pet_color", "pet_gender")


PetFilter.base_filters["pet_name"].label = "Pet Name"
PetFilter.base_filters["pet_breed"].label = "Pet Breed"


class UserFilter(django_filters.FilterSet):

    ny_choices = (
        ("Manhattan", "Manhattan"),
        ("Brooklyn", "Brooklyn"),
        ("Queens", "Queens"),
        ("Staten Island", "Staten Island"),
        ("Bronx", "Bronx"),
    )
    city = django_filters.ChoiceFilter(choices=ny_choices)
    username = django_filters.CharFilter(lookup_expr="icontains")
    first_name = django_filters.CharFilter(lookup_expr="icontains")
    last_name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "city")


UserFilter.base_filters["username"].label = "Username"
UserFilter.base_filters["first_name"].label = "First Name"
UserFilter.base_filters["last_name"].label = "Last Name"
