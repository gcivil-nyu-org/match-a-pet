import django_filters
from .models import ClientUserPet


class ClientPetFilter(django_filters.FilterSet):

    gender_choices = (("Male", "Male"), ("Female", "Female"))
    day_choices = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )
    time_choices = (
        ("Morning", "Morning"),
        ("Noon", "Noon"),
        ("Evening", "Evening"),
        ("Night", "Night"),
    )
    spayneuter_choices = (
        ("Yes", "Yes"),
        ("No", "No"),
    )
    pet_gender = django_filters.ChoiceFilter(choices=gender_choices)
    pet_playdate_day1 = django_filters.ChoiceFilter(choices=day_choices)
    pet_playdate_time1 = django_filters.ChoiceFilter(choices=time_choices)
    pet_spayneuter = django_filters.ChoiceFilter(choices=spayneuter_choices)
    pet_breed = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = ClientUserPet
        fields = ("pet_breed", "pet_gender", "pet_playdate_day1", "pet_playdate_time1")


ClientPetFilter.base_filters["pet_breed"].label = "Breed"
ClientPetFilter.base_filters["pet_gender"].label = "Gender"
ClientPetFilter.base_filters["pet_playdate_day1"].label = "Playdate Day"
ClientPetFilter.base_filters["pet_playdate_time1"].label = "Playdate Time"
ClientPetFilter.base_filters["pet_spayneuter"].label = "Spay/Neuter Status"
