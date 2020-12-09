from django.test import TestCase
from django.urls import reverse
from accounts.models import ShelterRegisterData, Pet, UserRegisterData, User, Message
from accounts.forms import (
    ShelterRegistrationForm,
    PetForm,
    # UserRegistrationForm,
    ShelterUserUpdateForm,
    ShelterUpdateForm,
    ClientUserUpdateForm,
    ClientUpdateForm,
)
from django.core.files.uploadedfile import SimpleUploadedFile


class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse("accounts:register")
        self.dummy_user = User.objects.create(
            username="peter7",
            email="peter@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        self.dummy_shelterRegisterData = ShelterRegisterData.objects.create(
            user=self.dummy_user,
            shelter_profile_image="default.jpg",
        )
        self.assertEqual(str(self.dummy_shelterRegisterData), "peter7")

        self.user = {
            "username": "peter7",
            "email": "peter@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password1": "test123abc",
            "password2": "test123abc",
        }
        self.user_no_username = {
            "username": "",
            "email": "peter@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password1": "test123abc",
            "password2": "test123abc",
        }

        self.user_name_exists = {
            "username": "peter7",
            "email": "peter@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password1": "test123abc",
            "password2": "test123abc",
        }

        self.user_email_exists = {
            "username": "peter7",
            "email": "peter@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password1": "test123abc",
            "password2": "test123abc",
        }

        self.user_hm_invalid_email = {
            "username": "peter7",
            "email": "pet@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password1": "test123abc",
            "password2": "test123abc",
        }

        return super().setUp


class ShelterRegisterFormTest(BaseTest):
    def test_form_not_valid(self):
        form = ShelterRegistrationForm(self.user_no_username)
        self.assertFalse(form.is_valid())

    def test_form_valid(self):
        form = ShelterRegistrationForm(self.user)
        self.assertFalse(form.is_valid())

    def test_form_username_exists(self):
        form = ShelterRegistrationForm(self.user_name_exists)
        form.has_error("username", "A user with that username already exists.")

    def test_form_email_exists(self):
        form = ShelterRegistrationForm(self.user_email_exists)
        form.has_error(
            "email",
            "This Email is already registered. "
            "Please use a different email address.",
        )

    def test_form_hm_invalid_email(self):
        form = ShelterRegistrationForm(self.user_hm_invalid_email)
        form.has_error(
            "This email is not a valid Email Address for Hiring Manager. "
            "Please use a different email address."
        )


# class UserRegisterFormTest(BaseTest):
#     def test_form_not_valid(self):
#         form = UserRegistrationForm(self.user_no_username)
#         self.assertFalse(form.is_valid())
#
#     def test_form_valid(self):
#         form = UserRegistrationForm(self.user)
#         self.assertFalse(form.is_valid())
#
#     def test_form_username_exists(self):
#         form = UserRegistrationForm(self.user_name_exists)
#         form.has_error("username", "A user with that username already exists.")
#
#     def test_form_email_exists(self):
#         form = UserRegistrationForm(self.user_email_exists)
#         form.has_error(
#             "email",
#             "This Email is already registered. "
#             "Please use a different email address.",
#         )
#
#     def test_form_hm_invalid_email(self):
#         form = UserRegistrationForm(self.user_hm_invalid_email)
#         form.has_error(
#             "This email is not a valid Email Address for Hiring Manager. "
#             "Please use a different email address."
#         )


class BaseTest2(TestCase):
    def test_save_shelter_profile_image_correctly(self):
        self.user = User.objects.create(
            username="peter7",
            email="peter@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        # self.client.login(username="huanjin", password="test123456")
        self.user.sprofile = ShelterRegisterData.objects.create(
            shelter_profile_image="default.jpg",
        )

        self.assertNotEqual(self.user.sprofile.shelter_profile_image.height, 301)
        self.assertNotEqual(self.user.sprofile.shelter_profile_image.width, 301)
        self.assertEqual(str(self.user.sprofile), "peter7")

    def test_save_user_profile_image_correctly(self):
        self.user = User.objects.create(
            username="peter7",
            email="peter@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        # self.client.login(username="huanjin", password="test123456")
        self.user.uprofile = UserRegisterData.objects.create(
            user_profile_image="default.jpg",
        )

        self.assertNotEqual(self.user.uprofile.user_profile_image.height, 301)
        self.assertNotEqual(self.user.uprofile.user_profile_image.width, 301)
        self.assertEqual(str(self.user.uprofile), "peter7 ClientUser Profile")

    def test_shelter_pet_relation_correctly(self):
        self.user = User.objects.create(
            username="peter7",
            email="peter@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        # self.client.login(username="huanjin", password="test123456")
        self.dummy_shelterRegisterData = ShelterRegisterData.objects.create(
            shelter_profile_image="default.jpg",
        )

        self.dummy_pet = Pet.objects.create(
            pet_name="Dog",
            pet_breed="Shihtzu",
            pet_age="4",
            pet_color="White",
            pet_gender="Female",
            pet_profile_image2="default.jpg",
            pet_profile_image3="default.jpg",
        )

        self.assertEqual(str(self.dummy_pet.pet_name), "Dog")
        self.assertEqual(self.dummy_pet.pet_gender, "Female")
        self.assertLessEqual(self.dummy_pet.pet_profile_image2.width, 300)
        self.assertLessEqual(self.dummy_pet.pet_profile_image2.height, 300)
        self.assertLessEqual(self.dummy_pet.pet_profile_image3.width, 300)
        self.assertLessEqual(self.dummy_pet.pet_profile_image3.height, 300)
        # self.assertEqual(str(self.user.uprofile), "peter7 ClientUser Profile")


# class BaseTest1(TestCase):
#     self.dummy_pet = Pet.objects.create(
#             pet_name="Sheila",
#             pet_breed="Dog",
#             pet_age="4",
#             pet_color="White",
#             pet_gender="Female",
#         )


# class BaseTest1(TestCase):
#     def setUp(self):
#         self.register_url = reverse("accounts:pet-register")
#         self.dummy_user = Pet.objects.create(
#             pet_name="Sheila",
#             pet_breed="Dog",
#             pet_age="4",
#             pet_color="White",
#             pet_gender="Female",
#         )

#         self.user = {
#             "pet_name": "Sheila",
#             "pet_breed": "Dog",
#             "pet_age": "4",
#             "pet_color": "White",
#             "pet_gender": "Female",
#         }
#         self.user_no_username = {
#             "pet_name": "Sheila",
#             "pet_breed": "Dog",
#             "pet_age": "4",
#             "pet_color": "White",
#             "pet_gender": "Female",
#         }

#         self.user_name_exists = {
#             "username": "peter7",
#             "email": "peter@matchapet.com",
#             "first_name": "Peter",
#             "last_name": "Voltz",
#             "shelter_city": "Manhattan",
#             "shelter_state": "New York",
#             "password1": "test123abc",
#             "password2": "test123abc",
#         }

#         self.user_email_exists = {
#             "username": "peter7",
#             "email": "peter@matchapet.com",
#             "first_name": "Peter",
#             "last_name": "Voltz",
#             "shelter_city": "Manhattan",
#             "shelter_state": "New York",
#             "password1": "test123abc",
#             "password2": "test123abc",
#         }

#         self.user_hm_invalid_email = {
#             "username": "peter7",
#             "email": "pet@matchapet.com",
#             "first_name": "Peter",
#             "last_name": "Voltz",
#             "shelter_city": "Manhattan",
#             "shelter_state": "New York",
#             "password1": "test123abc",
#             "password2": "test123abc",
#         }

#         return super().setUp
