from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import ShelterRegisterData, Pet, UserRegisterData, User, Message
from accounts.forms import (
    PetForm,
    ClientUserUpdateForm,
    ShelterUserUpdateForm,
    ShelterRegistrationForm,
)


class BaseTest(TestCase):
    def setUp(self):

        self.register_url = reverse("accounts:register")
        self.dummy_user = User.objects.create(
            # is_shelter=True,
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
        self.dummyy_user = User.objects.create(
            is_shelter=True,
            is_clientuser=False,
            username="peter77",
            email="peter@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            phone="124356789",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            latitude="12.90",
            longitude="13.47",
            password="test123abc",
        )
        self.dummy_shelterRegisterData = ShelterRegisterData.objects.create(
            user=self.dummy_user,
            shelter_profile_image="default.jpg",
        )
        self.assertEqual(str(self.dummy_shelterRegisterData), "peter7")

        self.user = {
            "is_shelter": True,
            "username": "peter7",
            "email": "peter@matchapet.com",
            "first_name": "Peter",
            "last_name": "Voltz",
            "address": "5th Ave",
            "city": "Manhattan",
            "state": "New York",
            "zip_code": "11209",
            "password": "test123abc",
            # "password2": "test123abc",
        }
        self.shelter_user = {
            "is_shelter": True,
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


class TestViews(TestCase):

    # ** Home View, Login View and Logout View
    def test_home_view(self):
        client = Client()

        response = client.get(reverse("accounts:accounts-home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")

    # def test_MatchUser_view(self):
    #     client = Client()
    #
    #     response = client.get(reverse("accounts:swiper"))
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, "accounts/swiper.html")

    def test_login_view(self):
        client = Client()

        response = client.get(reverse("accounts:login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_logout_view(self):
        client = Client()

        response = client.get(reverse("accounts:logout"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")

    def test_shelter_login_post_view(self):
        client = Client()

        response = client.post(reverse("accounts:login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_shelter_logout_post_view(self):
        client = Client()

        response = client.post(reverse("accounts:logout"), {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")

    # ** Shelter Views
    # def test_shelter_register_view(self):
    #     client = Client()
    #
    #     response = client.get(reverse("accounts:register-shelter"))
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, "accounts/register.html")

    def test_shelter_profile_view(self):
        client = Client()

        response = client.get(reverse("accounts:shelter-profile"))
        self.assertEquals(response.status_code, 302)

    # ** ClientUser Views
    def test_user_register_view(self):
        client = Client()

        response = client.get(reverse("accounts:register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_profile_view(self):
        client = Client()

        response = client.get(reverse("accounts:user-profile"))
        self.assertEquals(response.status_code, 302)

    # ** Pet Views
    def test_pet_register_view(self):
        client = Client()

        response = client.get(reverse("accounts:pet-register"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/pets.html")

    # ** User Views
    def test_shelter_register_post_view(self):
        client = Client()
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

        response = client.post(reverse("accounts:register"), {})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertEquals(str(self.dummy_user.email), "peter@matchapet.com")
        self.assertEquals(str(self.dummy_user.username), "peter7")
        self.assertEquals(str(self.dummy_user.first_name), "Peter")
        self.assertEquals(str(self.dummy_user.last_name), "Voltz")
        self.assertEquals(str(self.dummy_user.address), "5th Ave")
        self.assertEquals(str(self.dummy_user.city), "Manhattan")
        self.assertEquals(str(self.dummy_user.state), "New York")
        self.assertEquals(str(self.dummy_user.zip_code), "11209")

    def test_browse_view_pets(self):
        client = Client()
        response = client.get(reverse("accounts:view-pets"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/view_pets.html")

    def test_search(self):
        client = Client()
        response = client.get(reverse("accounts:search-user-shelters"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/searchShelterUser.html")

    def test_MatchUser_view(self):
        client = Client()

        response = client.get(reverse("accounts:swiper"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/swiper.html")

    def test_newconversation_view(self):
        client = Client()

        response = client.get(reverse("accounts:newconversation", args=["peter7"]))
        self.assertEquals(response.status_code, 302)

    def test_inbox_view(self):
        client = Client()
        user = User.objects.create(
            is_clientuser=True,
            username="peter8",
            email="pete@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        self.client.login(username="peter8", password="test123abc")

        messages = Message.get_messages(user=user)

        response = client.get(
            reverse("accounts:inbox"),
            {
                "directs": "directs",
                "active_direct": "active_direct",
                "messages": messages,
            },
        )
        self.assertEquals(response.status_code, 302)

    def test_shelter_profile(self):
        client = Client()
        response = client.post(reverse("accounts:shelter-profile"))
        self.assertEquals(response.status_code, 302)

    def test_user_profile(self):
        client = Client()

        response = client.post(reverse("accounts:user-profile"))
        self.assertEquals(response.status_code, 302)


class RegisterTestView(BaseTest):

    # Setup for the test

    def test_can_view_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_can_register_shelter(self):
        user_count = User.objects.count()
        response = self.client.post(
            self.register_url, self.shelter_user, format="text/html"
        )
        user_count = user_count + 1
        # self.assertEqual(User.objects.count(), user_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        # self.assertRedirects(
        #     response, reverse("accounts:login"), fetch_redirect_response=True
        # )

    def test_register_view_user_logged_in(self):
        user_login = self.client.login(
            username=self.dummyy_user.username, password="test123abc"
        )
        self.assertFalse(user_login)

    #     response = self.client.get(self.register_url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertRedirects(
    #         response, reverse("dashboard:dashboard"), fetch_redirect_response=False
    #     )


class TestProfile(TestCase):
    def setUp(self):
        self.petprofile_url = reverse("accounts:pet-profile", args=["1"])
        self.shelterprofile_url = reverse("accounts:shelterprofile", args=["peter7"])
        self.petregister_url = reverse("accounts:pet-register")
        self.favorites_url = reverse("accounts:favorite_pet", args=["1"])
        self.favoriteslist_url = reverse("accounts:favorite_list")

        self.test_pet = Pet.objects.create(
            id="1",
            pet_name="Dog",
            pet_breed="Shihtzu",
            pet_age="4",
            pet_color="White",
            pet_gender="Female",
            pet_profile_image1="default.jpg",
        )
        self.dummy_shelter = User.objects.create(
            is_shelter=True,
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

        self.dummy_user = User.objects.create(
            is_clientuser=True,
            username="peter8",
            email="pete@matchapet.com",
            first_name="Peter",
            last_name="Voltz",
            address="5th Ave",
            city="Manhattan",
            state="New York",
            zip_code="11209",
            password="test123abc",
        )
        self.form = ShelterUserUpdateForm(
            data={
                "about": "Hi",
                "username": "benjamin",
                "first_name": "ben",
                "last_name": "teo",
                "address": "123 Hope Street",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11201",
            }
        )

    def test_pet_profile(self):
        response = self.client.get(
            self.petprofile_url,
            {
                "pet": self.test_pet,
                "is_favorite": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/pet_profile.html")

    def test_pet_profile_favorite_true(self):
        is_favorite = True
        response = self.client.get(
            self.petprofile_url,
            {
                "pet": self.test_pet,
                "is_favorite": is_favorite,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/pet_profile.html")

    def test_shelter_profile(self):
        response = self.client.get(
            self.shelterprofile_url,
            {
                "user1": self.dummy_shelter,
                "pets": self.test_pet,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/shelter_profile.html")

    def test_pet_register(self):
        form_pet = PetForm(
            data={
                "shelterRegisterData": "peter7",
                "favorite": "False",
                "pet_name": "Tequila",
                "pet_breed": "Shiba",
                "pet_age": "Baby",
                "pet_color": "Black",
                "pet_gender": "Male",
                "pet_profile_image1": "image.jpg",
            }
        )
        instance = form_pet.save()
        instance.save()
        form_pet.save()

        response = self.client.post(
            self.petregister_url,
        )
        instance = form_pet.save()
        instance.save()
        form_pet.save()
        self.assertTrue(form_pet.is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/pets.html")

    def test_favorite_pet(self):
        self.client.login(username=self.dummy_user.username, password="test123abc")
        response = self.client.get(self.favorites_url)
        self.assertEqual(response.status_code, 302)

    def test_adoption(self):
        adoption_url = reverse("accounts:adopt_pending", args=["1"])
        response = self.client.get(adoption_url)
        self.assertEqual(response.status_code, 302)

    def test_adoption_cancelled(self):
        adoption_url = reverse("accounts:adopt_cancel", args=["1"])
        response = self.client.get(adoption_url)
        self.assertEqual(response.status_code, 302)

    def test_adoption_successful(self):
        adoption_url = reverse("accounts:adopt_complete", args=["1"])
        response = self.client.get(adoption_url)
        self.assertEqual(response.status_code, 302)

    def test_favorite_list(self):

        self.client.login(username="peter8", password="test123abc")
        favorites = self.dummy_user.favorite.all()
        response = self.client.get(self.favoriteslist_url, {"favorites": favorites})
        self.assertEqual(response.status_code, 302)

    def test_ShelterUserUpdateView(self):
        shelterupdate_url = reverse("accounts:shelter-profile")
        response = self.client.post(
            shelterupdate_url,
            data={
                "shelterUserUpdateForm": self.form,
                "shelterUpdateForm": self.form,
            },
        )
        self.assertEqual(response.status_code, 302)
        # self.assertTemplateUsed(response, "accounts/shelterProfile.html")

    def test_ShelterUpdateForm_is_valid(self):

        self.assertTrue(self.form.is_valid())

    def test_ClientUpdateForm_is_valid(self):
        form = ClientUserUpdateForm(
            data={
                "about": "Hi",
                "username": "benjamin1",
                "first_name": "ben",
                "last_name": "teo",
                "address": "123 Hope Street",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11201",
            }
        )
        self.assertTrue(form.is_valid())

    def test_registeruser(self):
        usersignup = reverse("accounts:register")

        response = self.client.post(usersignup)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_registershelter(self):
        sheltersignup = reverse("accounts:register")

        response = self.client.post(sheltersignup)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    # def test_registershelter1(self):
    #     sheltersignup = reverse("accounts:register")
    #     self.user = {
    #         "username": "test",
    #         "email": "testemail@gmail.com",
    #         "first_name": "first",
    #         "last_name": "last",
    #         "password1": "123456test",
    #         "password2": "123456test",
    #     }
    #     response = self.client.post(sheltersignup, self.user, format="text/html")
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "accounts/register.html")


# class TestUserRegisterView(TestCase):
#     def test_view_register_page(self):
#         client = Client()

#         self.dummy_user = User.objects.create(
#                     username="peter7",
#                     email="peter@matchapet.com",
#                     first_name="Peter",
#                     last_name="Voltz",
#                     address="5th Ave",
#                     city="Manhattan",
#                     state="New York",
#                     zip_code="11209",
#                     password="test123abc",
#                 )

#         self.dummy_shelterRegisterData = ShelterRegisterData.objects.create(
#             user=self.dummy_user,
#             shelter_profile_image="default.jpg",
#         )

#         self.dummy_pet = Pet.objects.create(
#             shelterRegisterData = self.dummy_shelterRegisterData,
#             pet_name="Dog",
#             pet_breed="Shihtzu",
#             pet_age="4",
#             pet_color="White",
#             pet_gender="Female",
#         )

#         client.login(username=self.dummy_user.username, password="test123abc")
#         # response = client.get(reverse("accounts:pet-register"))
#         self.url = reverse("accounts:pet-register")
#         response = client.post(
#             self.url,
#             {
#                 "pet_name": "Sheila",
#                 "pet_breed": "Dog",
#                 "pet_age": "Baby",
#                 "pet_color": "White",
#                 "pet_gender": "Female",
#                 "pet_profile_image1": "default.jpg",
#                 "pet_profile_image2": "default.jpg",
#                 "pet_profile_image3": "default.jpg",
#             },
#         )
#         self.assertEqual(response.status_code, 200)

# def test_shelter_register_post_view1(self):
#     client = Client()
#     self.registerURL = reverse("accounts:register-shelter")
#     self.dummy_user = ShelterRegisterData.objects.create(
#         # shelter_id=5,
#         username="peter7",
#         email="peter@matchapet.com",
#         first_name="Peter",
#         last_name="Voltz",
#         shelter_city="Manhattan",
#         shelter_state="New York",
#         password="test123abc",
#     )

#     response = client.post(
#         self.registerURL,
#         {
#             "username": "peter7",
#             "email": "peter@matchapet.com",
#             "first_name": "Peter",
#             "last_name": "Voltz",
#             "shelter_city": "Manhattan",
#             "shelter_state": "New York",
#             "password1": "test123abc",
#             "password2": "test123abc",
#         },
#     )
#     self.assertEquals(response.status_code, 200)
#     self.assertTemplateUsed(response, "accounts/register.html")
#     self.assertEquals(str(self.dummy_user.email), "peter@matchapet.com")
#     self.assertEquals(str(self.dummy_user.username), "peter7")
#     self.assertEquals(str(self.dummy_user.first_name), "Peter")
#     self.assertEquals(str(self.dummy_user.last_name), "Voltz")
#     self.assertEquals(str(self.dummy_user.shelter_state), "New York")

# def test_shelter_update_post_view1(self):
#     client = Client()
#     self.registerURL = reverse("accounts:shelter-profile")
#     self.dummy_user = ShelterRegisterData.objects.create(
#         # shelter_id=5,
#         username="peter7",
#         email="peter@matchapet.com",
#         first_name="Peter",
#         last_name="Voltz",
#         shelter_city="Manhattan",
#         shelter_state="New York",
#         password="test123abc",
#     )

#     shelterid = ShelterRegisterData.objects.get(email="peter@matchapet.com")

#     response = client.post(self.registerURL, {})
#     self.assertEquals(response.status_code, 302)
#     self.assertEquals(shelterid.username, "peter7")
#     self.assertEquals(shelterid.email, "peter@matchapet.com")
#     self.assertEquals(str(self.dummy_user.email), "peter@matchapet.com")
#     self.assertEquals(str(self.dummy_user.username), "peter7")
#     self.assertEquals(str(self.dummy_user.first_name), "Peter")
#     self.assertEquals(str(self.dummy_user.last_name), "Voltz")
#     self.assertEquals(str(self.dummy_user.shelter_state), "New York")

# def test_pet_register_post_view(self):
#     client = Client()
#     self.dummy_user = ShelterRegisterData.objects.create(
#         email="peter@matchapet.com",
#     )
#     self.dummy_pet = Pet.objects.create(
#         id=self.dummy_user,
#         # pet_id="5",
#         pet_name="Sheila",
#         pet_breed="Dog",
#         pet_age="4",
#         pet_color="White",
#         pet_gender="Female",
#         # date_entered="12/1/2020",
#     )

#     petid = Pet.objects.get(pet_name="Sheila")
#     # shelterid = ShelterRegisterData.objects.get(shelter_id=5)

#     response = client.post(reverse("accounts:pet-register"), {})
#     self.assertEquals(response.status_code, 200)
#     self.assertEquals(str(petid.id), "peter@matchapet.com")
#     self.assertTemplateUsed(response, "accounts/pets.html")
#     self.assertEquals(str(self.dummy_pet.id), "peter@matchapet.com")

# def test_pet_register_post_view1(self):
#     client = Client()
#     self.dummy_user = ShelterRegisterData.objects.create(
#         email="peter@matchapet.com",
#     )
#     self.dummy_pet = Pet.objects.create(
#         email=self.dummy_user,
#         pet_id="5",
#         pet_name="Sheila",
#         pet_breed="Dog",
#         pet_age="4",
#         pet_color="White",
#         pet_gender="Female",
#         date_entered="12/1/2020",
#     )

#     response = client.post(reverse("accounts:pet-register"), {
#         "email":"peter@matchapet.com",
#         "pet_name": "Sheila",
#         "pet_breed": "Dog",
#         "pet_age": "4",
#         "pet_color": "White",
#         "pet_gender": "Female",
#         "date_entered": "12/1/2020",
#     })

#     petid = Pet.objects.get(pet_id=5)

#     self.assertEquals(response.status_code, 200)
#     self.assertTemplateUsed(response, "accounts/pets.html")
#     self.assertEquals(str(self.dummy_pet.email), "peter@matchapet.com")
#     self.assertEquals(self.dummy_pet.pet_name, "pet_name")
class RegistrationTests(TestCase):
    def test_usertype_label(self):
        form = ShelterRegistrationForm()
        self.assertTrue(
            form.fields["user_type"].label == "Are You A Shelter Or A User?"
        )

    def test_username_label(self):
        form = ShelterRegistrationForm()
        self.assertTrue(
            form.fields["username"].label == "Name of Shelter or Username for User"
        )

    def test_email_label(self):
        form = ShelterRegistrationForm()
        self.assertTrue(form.fields["email"].label == "Email Address")

    # def test_password_label(self):
    #     form = ShelterRegistrationForm()
    #     self.assertTrue(form.fields["password1"].label == "")
    #
    # def test_password2_label(self):
    #     form = ShelterRegistrationForm()
    #     self.assertTrue(form.fields["password2"].label == "")

    # def test_city_label(self):
    #     form = ShelterRegistrationForm()
    #     self.assertTrue(form.fields["city"].label == "")
    #
    # def test_state_label(self):
    #     form = ShelterRegistrationForm()
    #     self.assertTrue(form.fields["state"].label == "")

    def test_form_working(self):
        form = ShelterRegistrationForm(
            data={
                "user_type": "Shelter",
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "address": "5th Ave",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11209",
                "password1": "test123abc",
                "password2": "test123abc",
            }
        )
        self.assertTrue(form.is_valid())

    def test_successful_post_shelter_request(self):
        form = self.client.post(
            reverse("accounts:register"),
            data={
                "user_type": "Shelter",
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "address": "5th Ave",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11209",
                "password1": "test123abc",
                "password2": "test123abc",
            },
        )
        self.assertEqual(form.status_code, 302)

    def test_successful_shelter_update(self):
        form = self.client.post(
            reverse("accounts:shelter-profile"),
            data={
                "about": "Hi",
                "username": "benjamin",
                "first_name": "ben",
                "last_name": "teo",
                "address": "123 Hope Street",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11201",
            },
        )
        self.assertEqual(form.status_code, 302)

    def test_successful_user_update(self):
        form = self.client.post(
            reverse("accounts:user-profile"),
            data={
                "about": "Hi",
                "username": "benjamin",
                "first_name": "ben",
                "last_name": "teo",
                "address": "123 Hope Street",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "11201",
            },
        )
        self.assertEqual(form.status_code, 302)
