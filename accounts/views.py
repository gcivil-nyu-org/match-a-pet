from django.urls import reverse
from django.contrib import messages
from .forms import (
    ShelterRegistrationForm,
    PetForm,
    UserRegistrationForm,
    ShelterUserUpdateForm,
    ShelterUpdateForm,
    ClientUserUpdateForm,
    ClientUpdateForm,
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import account_activation_token
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django_tables2 import SingleTableView
from .models import Pet, ShelterRegisterData, User
from .tables import PetTable
from django.template import loader
from .filters import PetFilter
from django.core.paginator import Paginator
import requests

global form


def home(request):
    return render(request, "accounts/home.html")


def registerShelter(request):
    if request.method == "POST":

        form = ShelterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_shelter = True

            coord = []
            coord = add_to_geo(user.state, user.city, user.address)
            user.latitude = coord[0]
            user.longitude = coord[1]

            user.save()
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            current_site = get_current_site(request)
            email_subject = "Please activate your account on Match A Pet"
            email_body = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            link = reverse(
                "accounts:activate",
                kwargs={"uidb64": email_body["uid"], "token": email_body["token"]},
            )
            activate_url = "http://" + current_site.domain + link

            send_mail(
                email_subject,
                "Hi "
                + first_name
                + " "
                + last_name
                + ", Please the link below to activate your account: \n"
                + activate_url,
                "nyu-match-a-pet@gmail.com",
                [email],
            )

            messages.success(
                request,
                "Account successfully created. Please check your email to verify your account.",
            )
            return redirect("/login")
    else:
        form = ShelterRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def registerUser(request):
    if request.method == "POST":

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.is_clientuser = True
            user.save()
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            current_site = get_current_site(request)
            email_subject = "Please activate your account on Match A Pet"
            email_body = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }
            link = reverse(
                "accounts:activate",
                kwargs={"uidb64": email_body["uid"], "token": email_body["token"]},
            )
            activate_url = "http://" + current_site.domain + link

            send_mail(
                email_subject,
                "Hi "
                + first_name
                + " "
                + last_name
                + ", Please the link below to activate your account: \n"
                + activate_url,
                "nyu-match-a-pet@gmail.com",
                [email],
            )

            messages.success(
                request,
                "Account successfully created. Please check your email to verify your account.",
            )
            return redirect("/login")
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def loginShelter(request):
    return render(request, "accounts/login.html")


def petProfile(request, id):
    pet = get_object_or_404(Pet, id=id)
    is_favorite = False
    if pet.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    context = {
        "pet": pet,
        "is_favorite": is_favorite,
    }

    template = loader.get_template("accounts/pet_profile.html")

    return HttpResponse(template.render(context, request))


def shelter_profile(request, username):
    shelteruser = User.objects.get(username=username)
    pets = Pet.objects.filter(shelterRegisterData_id=shelteruser.id).all()
    context = {
        "user1": shelteruser,
        "pet_list": pets,
    }

    template = loader.get_template("accounts/shelter_profile.html")

    return HttpResponse(template.render(context, request))


class PetListView(ListView):  # method we will use to load tables into View Pets
    model = Pet
    # table_class = PetTable
    template_name = "accounts/view_pets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PetFilter(self.request.GET, queryset=self.get_queryset())
        return context

    paginate_by = 5


def petsRegister(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shelterRegisterData = request.user.sprofile
            instance.save()
            form.save()
            pet = form.cleaned_data.get("pet_name")
            messages.success(request, f"Pet profile created for {pet}!")
            return render(request, "accounts/pets.html", {"form": form})

    else:
        form = PetForm()
    return render(request, "accounts/pets.html", {"form": form})


@login_required
def favorite_pet(request, id):
    pet = get_object_or_404(Pet, id=id)
    if pet.favorite.filter(id=request.user.id).exists():
        pet.favorite.remove(request.user)
    else:
        pet.favorite.add(request.user)

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def favorites_list(request):
    user = request.user
    favorites = user.favorite.all()
    context = {
        "favorites": favorites,
    }
    return render(request, "accounts/favorite.html", context)


@login_required
def shelterProfile(request):
    if request.method == "POST":
        shelterUserUpdateForm = ShelterUserUpdateForm(
            request.POST, instance=request.user
        )
        shelterUpdateForm = ShelterUpdateForm(
            request.POST, request.FILES, instance=request.user.sprofile
        )
        if shelterUserUpdateForm.is_valid() and shelterUpdateForm.is_valid():
            shelterUserUpdateForm.save()
            shelterUpdateForm.save()
            messages.success(request, "Account succesfully updated!")
            return redirect("/shelter/profile")
    else:
        shelterUserUpdateForm = ShelterUserUpdateForm(instance=request.user)
        shelterUpdateForm = ShelterUpdateForm(instance=request.user.sprofile)

    context = {
        "shelterUserUpdateForm": shelterUserUpdateForm,
        "shelterUpdateForm": shelterUpdateForm,
    }

    return render(request, "accounts/shelterProfile.html", context)


@login_required
def clientuserProfile(request):
    if request.method == "POST":
        clientUserUpdateForm = ClientUserUpdateForm(request.POST, instance=request.user)
        clientUpdateForm = ClientUpdateForm(
            request.POST, request.FILES, instance=request.user.uprofile
        )
        if clientUserUpdateForm.is_valid() and clientUpdateForm.is_valid():
            clientUserUpdateForm.save()
            clientUpdateForm.save()
            messages.success(request, "Account succesfully updated!")
            return redirect("/user/profile")
    else:
        clientUserUpdateForm = ClientUserUpdateForm(instance=request.user)
        clientUpdateForm = ClientUpdateForm(instance=request.user.uprofile)

    context = {
        "clientUserUpdateForm": clientUserUpdateForm,
        "clientUpdateForm": clientUpdateForm,
    }

    return render(request, "accounts/userProfile.html", context)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account successfully verified")
            return redirect("/login/")
        else:
            messages.success(request, "Activation link is invalid")
            return redirect("/login/")


def add_to_geo(state, city, address):
    api_key = "AIzaSyC796wfP4gXyVbNt2wpSW6zMUojqenu04w"
    city = city.replace(" ", "+")
    address = address.replace(" ", "+")
    response = requests.get(
        f"https://maps.googleapis.com/maps/api/geocode/json?address={address},+{city},+{state}&key={api_key}"
    )
    resp_json_payload = response.json()
    coordinates = ["null", "null"]
    coordinates[0] = resp_json_payload["results"][0]["geometry"]["location"]["lat"]
    coordinates[1] = resp_json_payload["results"][0]["geometry"]["location"]["lng"]
    # print(resp_json_payload["results"][0]["geometry"]["location"]["lat"])
    # print(resp_json_payload["results"][0]["geometry"]["location"]["lng"])
    return coordinates
