from django.urls import path
from . import views
from .views import PetListView, SearchShelterAndUserView, MatchUserView
from django.contrib.auth import views as auth_views
from .views import VerificationView

app_name = "accounts"
urlpatterns = [
    # path("search/", views.search, name="search"),
    path("", views.home, name="accounts-home"),
    # path("shelter/register/", views.registerShelter, name="register-shelter"),
    # path("user/register/", views.registerUser, name="register-user"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="accounts/home.html"),
        name="logout",
    ),
    path("shelter/profile/", views.shelterProfile, name="shelter-profile"),
    path("user/profile/", views.clientuserProfile, name="user-profile"),
    path("pets/register/", views.petsRegister, name="pet-register"),
    path("activate/<uidb64>/<token>", VerificationView.as_view(), name="activate"),
    path("view_pets/", PetListView.as_view(), name="view-pets"),
    path("profiles/", SearchShelterAndUserView.as_view(), name="search-user-shelters"),
    path("pets/<id>/", views.petProfile, name="pet-profile"),
    path("profile/<username>/", views.shelter_profile, name="shelterprofile"),
    path("favorite/<int:id>/", views.favorite_pet, name="favorite_pet"),
    path("user/favorites", views.favorites_list, name="favorite_list"),
    path("inbox/", views.inbox, name="inbox"),
    path("inbox/<username>", views.Directs, name="directs"),
    path("send/", views.SendDirect, name="send_direct"),
    path("send/new/<username>/", views.NewConversation, name="newconversation"),
    path("user/swiper/", views.MatchUserView.as_view(), name="swiper"),
    path("adoptpending/<int:id>/", views.adopt_pending, name="adopt_pending"),
    path("adoptcancel/<int:id>/", views.adopt_cancel, name="adopt_cancel"),
    path("adoptcomplete/<int:id>/", views.adopt_complete, name="adopt_complete"),
]
