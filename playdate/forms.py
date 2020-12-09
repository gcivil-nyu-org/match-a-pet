from django import forms
from .models import ClientUserPet


class ClientUserPetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pet_playdate_day1"].label = "Preferred Playdate Day"
        self.fields["pet_playdate_time1"].label = "Preferred Playdate Time"
        self.fields["pet_spayneuter"].label = "Spay/Neuter Status"

    # shelter_id = forms.CharField(disabled = True)
    # email = forms.CharField(disabled = True)
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    age_choices = (
        ("Baby", "Baby"),
        ("Young", "Young"),
        ("Adult", "Adult"),
        ("Senior", "Senior"),
    )
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

    pet_age = forms.ChoiceField(choices=age_choices)
    pet_gender = forms.ChoiceField(choices=gender_choices)
    pet_spayneuter = forms.ChoiceField(choices=spayneuter_choices)
    pet_playdate_day1 = forms.ChoiceField(choices=day_choices)
    pet_playdate_time1 = forms.ChoiceField(choices=time_choices)

    class Meta:
        model = ClientUserPet
        fields = [
            "pet_name",
            "pet_breed",
            "pet_age",
            "pet_color",
            "pet_gender",
            "pet_spayneuter",
            "pet_playdate_day1",
            "pet_playdate_time1",
            # "date_entered",
            "pet_profile_image1",
            "pet_profile_image2",
            "pet_profile_image3",
        ]
        labels = {
            "pet_profile_image1": ("Pet Profile Picture 1"),
            "pet_profile_image2": ("Pet Profile Picture 2"),
            "pet_profile_image3": ("Pet Profile Picture 3"),
        }
