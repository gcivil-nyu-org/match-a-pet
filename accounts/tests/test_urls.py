from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import (
    # registerShelter,
    shelterProfile,
    # registerUser,
    register,
    petsRegister,
    PetListView,
    VerificationView,
    SearchShelterAndUserView,
    petProfile,
    shelter_profile,
    inbox,
    Directs,
    SendDirect,
    NewConversation,
    checkDirects,
    MatchUserView,
)
from django.contrib.auth.views import LoginView, LogoutView


class TestUrls(SimpleTestCase):
    def test_shelter_register_url(self):
        url = reverse("accounts:register")
        self.assertEquals(resolve(url).func, register)
        self.assertEquals(resolve(url).route, "register/")

    # def test_user_register_url(self):
    #     url = reverse("accounts:register-user")
    #     self.assertEquals(resolve(url).func, registerUser)
    #     self.assertEquals(resolve(url).route, "user/register/")

    def test_shelter_login_url(self):
        url = reverse("accounts:login")
        self.assertEquals(resolve(url).func.view_class, LoginView)
        self.assertEquals(resolve(url).route, "login/")

    def test_shelter_logout_url(self):
        url = reverse("accounts:logout")
        self.assertEquals(resolve(url).func.view_class, LogoutView)
        self.assertEquals(resolve(url).route, "logout/")

    def test_shelter_profile_url(self):
        url = reverse("accounts:shelter-profile")
        self.assertEquals(resolve(url).func, shelterProfile)
        self.assertEquals(resolve(url).route, "shelter/profile/")

    def test_pet_register_url(self):
        url = reverse("accounts:pet-register")
        self.assertEquals(resolve(url).func, petsRegister)
        self.assertEquals(resolve(url).route, "pets/register/")

    def test_pets_view_url(self):
        url = reverse("accounts:view-pets")
        self.assertEquals(resolve(url).func.view_class, PetListView)
        self.assertEquals(resolve(url).route, "view_pets/")

    def test_pets_profile_url(self):
        url = reverse("accounts:pet-profile", args=["2"])
        self.assertEquals(resolve(url).func, petProfile)
        self.assertEquals(resolve(url).route, "pets/<id>/")

    def test_shelterprofile_url(self):
        url = reverse("accounts:shelterprofile", args=["peter7"])
        self.assertEquals(resolve(url).func, shelter_profile)
        self.assertEquals(resolve(url).route, "profile/<username>/")

    def test_email_activate_url(self):
        url = reverse("accounts:activate", args=["avhhk4ll2lbl2", "67172"])
        self.assertEquals(resolve(url).func.view_class, VerificationView)
        self.assertEquals(resolve(url).route, "activate/<uidb64>/<token>")

    def test_shelteruser_profiles(self):
        url = reverse("accounts:search-user-shelters")
        self.assertEquals(resolve(url).func.view_class, SearchShelterAndUserView)
        self.assertEquals(resolve(url).route, "profiles/")

    def test_swiper(self):
        url = reverse("accounts:swiper")
        self.assertEquals(resolve(url).func.view_class, MatchUserView)
        self.assertEquals(resolve(url).route, "user/swiper/")
