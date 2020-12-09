from django.shortcuts import render
import requests
from django.core import serializers
from accounts.models import User

# Google API KEY AIzaSyC796wfP4gXyVbNt2wpSW6zMUojqenu04w

mapbox_access_token = "pk.eyJ1Ijoic2hvcm5idWNrbGU5MyIsImEiOiJja2g5b3QxZnEwM3V3MnprM3gxZzlnMTlnIn0.U0IY_rRntdyeFAnW7bCSIQ"


def map_func(request):
    user1 = User.objects.all()
    # print(user[450].longitude)
    # return render(
    #     request,
    #     'map/maps-shelters.html',
    #     {
    #         'mapbox_access_token': mapbox_access_token,
    #         'user': user,
    #     })

    return render(
        request,
        "map/maps-shelters.html",
        {
            "mapbox_access_token": mapbox_access_token,
            "user1": user1,
        },
    )
