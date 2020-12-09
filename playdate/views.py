from django.shortcuts import render
from accounts.models import User
from django.contrib import messages
from .forms import ClientUserPetForm
from .models import ClientUserPet
from django.views.generic import ListView
from .filters import ClientPetFilter
from django.template import loader
from django.http import HttpResponse


def playdate_test(request):

    user = User.objects.all()
    return render(
        request,
        "map/map-test2.html",
        {
            "user": user,
        },
    )


def clientUserPetsRegister(request):
    if request.method == "POST":
        form = ClientUserPetForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.userRegisterData = request.user.uprofile
            instance.save()
            form.save()
            pet = form.cleaned_data.get("pet_name")
            messages.success(request, f"Pet profile created for {pet}!")
            return render(request, "playdate/petRegister.html", {"form": form})

    else:
        form = ClientUserPetForm()
    return render(request, "playdate/petRegister.html", {"form": form})


# @login_required
def my_pets_list(request, username):
    # user = request.user
    clientuser = User.objects.get(username=username)
    clientUserPet = ClientUserPet.objects.filter(
        userRegisterData_id=clientuser.id
    ).all()
    context = {
        "clientUserPet": clientUserPet,
    }
    return render(request, "playdate/myPets.html", context)


# def user_profile(request, username):
#     clientuser = User.objects.get(username=username)
#     pets = ClientUserPet.objects.filter(userRegisterData_id=clientuser.id).all()
#     context = {
#         "user1": clientuser,
#         "pet_list": pets,
#     }
#
#     template = loader.get_template("playdate/userProfile.html")
#
#     return HttpResponse(template.render(context, request))


class playDateView(ListView):  # method we will use to load tables into View Pets
    model = ClientUserPet
    # table_class = PetTable
    template_name = "playdate/playDateViewPets.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = ClientPetFilter(
            self.request.GET, queryset=self.get_queryset()
        )
        return context

    paginate_by = 5
