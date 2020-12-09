from django.urls import reverse
from django.contrib import messages
from .forms import (
    ShelterRegistrationForm,
    PetForm,
    # UserRegistrationForm,
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
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django_tables2 import SingleTableView
from .models import Pet, ShelterRegisterData, User, Message, UserRegisterData
from .tables import PetTable
from django.template import loader
from .filters import PetFilter, UserFilter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from playdate.views import ClientUserPet
from playdate.models import ClientUserPet

global form


def home(request):
    shelters = User.objects.filter(is_shelter=True).count()
    pets = Pet.objects.all().count()
    users = User.objects.filter(is_clientuser=True).count()
    adopted = Pet.objects.filter(pet_adoption_status=True).count()
    context = {
        "shelters": shelters,
        "pets": pets,
        "users": users,
        "adopted": adopted,
    }
    return render(request, "accounts/home.html", context)


def register(request):
    if request.method == "POST":

        form = ShelterRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user_type = form.cleaned_data.get("user_type")
            if user_type == "Shelter":
                user.is_shelter = True
            elif user_type == "User":
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
        form = ShelterRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


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
    client_pets = ClientUserPet.objects.filter(userRegisterData_id=shelteruser.id)
    ruser = request.user
    context = {
        "user1": shelteruser,
        "pet_list": pets,
        "ruser": ruser,
        "client_pets": client_pets,
    }

    template = loader.get_template("accounts/shelter_profile.html")

    return HttpResponse(template.render(context, request))


class PetListView(ListView):  # method we will use to load tables into View Pets
    model = Pet
    # paginate_by = 5
    template_name = "accounts/view_pets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = PetFilter(self.request.GET, queryset=self.get_queryset())
        context["filer_qs"] = context["filter"].qs

        paginator = Paginator(context["filer_qs"], 16)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj

        return context


class SearchShelterAndUserView(ListView):
    model = User

    template_name = "accounts/searchShelterUser.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = UserFilter(self.request.GET, queryset=self.get_queryset())
        context["filer_qs"] = context["filter"].qs

        paginator = Paginator(context["filer_qs"], 16)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj

        return context


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


# below method will update the pet model when user clicks adoption button.
@login_required
def adopt_pending(request, id):
    pet = get_object_or_404(Pet, id=id)
    # if pet.pet_pending_status == False:
    if not pet.pet_pending_status:
        pet.pet_pending_status = True
        pet.save()
        pet.pet_pending_user.add(request.user)

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# the below method will cancel a pending adoption
@login_required
def adopt_cancel(request, id):
    pet = get_object_or_404(Pet, id=id)
    pet.pet_pending_status = False
    pet.save()
    pet.pet_pending_user.remove()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


# the below method will complete an adoption
@login_required
def adopt_complete(request, id):
    pet = get_object_or_404(Pet, id=id)
    pet.pet_pending_status = False
    pet.pet_adoption_status = True
    pet.save()
    adoptee = pet.pet_pending_user.get()
    uregdata = UserRegisterData.objects.get(pk=adoptee.id)

    ClientUserPet.objects.create(
        pet_name=pet.pet_name,
        pet_breed=pet.pet_breed,
        pet_age=pet.pet_age,
        pet_gender=pet.pet_gender,
        pet_profile_image1=pet.pet_profile_image1,
        userRegisterData=uregdata,
    )

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


class MatchUserView(SingleTableView):
    # method we will be used to load tables into swiper feature
    model = Pet
    table_class = PetTable
    template_name = "accounts/swiper.html"
    paginate_by = 1


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


@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message["user"].username
        directs = Message.objects.filter(user=user, recipient=message["user"])
        directs.update(is_read=True)

        for message in messages:
            if message["user"].username == active_direct:
                message["unread"] = 0
    context = {"directs": directs, "messages": messages, "active_direct": active_direct}

    template = loader.get_template("accounts/messages.html")

    return HttpResponse(template.render(context, request))


@login_required
def Directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message["user"].username == username:
            message["unread"] = 0

    context = {"directs": directs, "messages": messages, "active_direct": active_direct}

    template = loader.get_template("accounts/messages.html")

    return HttpResponse(template.render(context, request))


@login_required
def SendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get("to_user")
    body = request.POST.get("body")

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect("accounts:inbox")
    else:
        HttpResponseBadRequest()


@login_required
def NewConversation(request, username):
    from_user = request.user
    body = "Hello!"
    to_user = User.objects.get(username=username)

    if from_user != to_user:
        Message.send_message(from_user, to_user, body)

    return redirect("accounts:inbox")


def checkDirects(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user, is_read=False).count()

    return {"directs_count": directs_count}
