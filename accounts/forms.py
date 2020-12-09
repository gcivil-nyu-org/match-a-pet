from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ShelterRegisterData, Pet, UserRegisterData, User


class ShelterRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_type"].label = "Are You A Shelter Or A User?"
        self.fields["email"].label = "Email Address"
        self.fields["username"].label = "Name of Shelter or Username for User"
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"

    l_choices = (("ny", "New York"), ("ca", "California"))
    ny_choices = (
        ("Manhattan", "Manhattan"),
        ("Brooklyn", "Brooklyn"),
        ("Queens", "Queens"),
        ("Staten Island", "Staten Island"),
        ("Bronx", "Bronx"),
    )
    user_choices = (
        ("Shelter", "Shelter"),
        ("User", "User"),
    )

    user_type = forms.ChoiceField(choices=user_choices)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    city = forms.ChoiceField(choices=ny_choices)
    state = forms.ChoiceField(choices=l_choices)
    zip_code = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "user_type",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip_code",
            "password1",
            "password2",
        ]
        help_texts = {
            "username": ("Input can contain Letters, digits and @/./+/-/_ only.")
        }


class ShelterUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["about"].label = "Your Bio"
        self.fields["username"].label = "Shelter Name"
        self.fields["first_name"].label = "Shelter Staff First Name"
        self.fields["last_name"].label = "Shelter Staff Last Name"

    l_choices = (("ny", "New York"), ("ca", "California"))
    ny_choices = (
        ("Manhattan", "Manhattan"),
        ("Brooklyn", "Brooklyn"),
        ("Queens", "Queens"),
        ("Staten Island", "Staten Island"),
        ("Bronx", "Bronx"),
    )

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.ChoiceField(choices=ny_choices)
    state = forms.ChoiceField(choices=l_choices)
    zip_code = forms.CharField(required=True)
    about = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "about",
            "username",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip_code",
        ]
        help_texts = {
            "username": ("Shelter name can contain Letters, digits and @/./+/-/_ only.")
        }


class ShelterUpdateForm(forms.ModelForm):
    class Meta:
        model = ShelterRegisterData
        fields = ["shelter_profile_image"]
        labels = {"shelter_profile_image": ("Shelter Profile Picture")}


class ClientUserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["about"].label = "Your Bio"
        self.fields["username"].label = "Username"
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"

    l_choices = (("ny", "New York"), ("ca", "California"))
    ny_choices = (
        ("Manhattan", "Manhattan"),
        ("Brooklyn", "Brooklyn"),
        ("Queens", "Queens"),
        ("Staten Island", "Staten Island"),
        ("Bronx", "Bronx"),
    )

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    city = forms.ChoiceField(choices=ny_choices)
    state = forms.ChoiceField(choices=l_choices)
    zip_code = forms.CharField(required=True)
    about = forms.CharField(required=False)

    class Meta:
        model = User
        fields = [
            "about",
            "username",
            "first_name",
            "last_name",
            "address",
            "city",
            "state",
            "zip_code",
        ]
        help_texts = {
            "username": ("Shelter name can contain Letters, digits and @/./+/-/_ only.")
        }


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = UserRegisterData
        fields = ["user_profile_image"]
        labels = {"user_profile_image": ("User Profile Picture")}


class PetForm(forms.ModelForm):

    # shelter_id = forms.CharField(disabled = True)
    # email = forms.CharField(disabled = True)
    gender_choices = (("Male", "Male"), ("Female", "Female"))
    age_choices = (
        ("Baby", "Baby"),
        ("Young", "Young"),
        ("Adult", "Adult"),
        ("Senior", "Senior"),
    )

    pet_age = forms.ChoiceField(choices=age_choices)
    pet_gender = forms.ChoiceField(choices=gender_choices)

    class Meta:
        model = Pet
        fields = [
            "pet_name",
            "pet_breed",
            "pet_age",
            "pet_color",
            "pet_gender",
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
