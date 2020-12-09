from django.urls import path

from playdate.views import playDateView
from . import views

app_name = "playdate"
urlpatterns = [
    path("playdate/test/", views.playdate_test, name="play-date"),
    path("user/petregister/", views.clientUserPetsRegister, name="user-pet-register"),
    path("playdates/", playDateView.as_view(), name="playdates"),
    # path("userprofile/<username>/", views.user_profile, name="userprofile"),
    path("user/mypets/<username>/", views.my_pets_list, name="my_pets"),
]
