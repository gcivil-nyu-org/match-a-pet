from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models import Max

# User has fields address, city, date_joined, email, first_name,
# groups, id, is_active, is_clientuser, is_shelter, is_staff, is_superuser,
# last_login, last_name, logentry, password, phone, sprofile, state,
# uprofile, user_permissions, username, zip_code, latitude, longitude


class User(AbstractUser):
    is_shelter = models.BooleanField("shelter status", default=False)
    is_clientuser = models.BooleanField("clientuser status", default=False)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=5, blank=True)
    latitude = models.CharField(max_length=20, blank=True)
    longitude = models.CharField(max_length=20, blank=True)
    about = models.CharField(max_length=1000, blank=True)


# ShelterRegisterData has fields pet, shelter_profile_image, user, user_id
class ShelterRegisterData(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="sprofile"
    )
    shelter_profile_image = models.ImageField(
        default="default.jpg", upload_to="shelter_profile_pics", blank=True
    )

    def __str__(self):
        return f"{self.user.username}"

    def save(self, *args, **kwargs):
        super(ShelterRegisterData, self).save(*args, **kwargs)

        img = Image.open(self.shelter_profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.shelter_profile_image.path)


# UserRegisterData has fields user, user_id, user_profile_image
class UserRegisterData(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="uprofile"
    )
    user_profile_image = models.ImageField(
        default="default.jpg", upload_to="user_profile_pics", blank=True
    )

    def __str__(self):
        return f"{self.user.username} ClientUser Profile"

    def save(self, *args, **kwargs):
        super(UserRegisterData, self).save(*args, **kwargs)
        img = Image.open(self.user_profile_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.user_profile_image.path)


# Pet has fields id, pet_age, pet_breed, pet_color, pet_gender, pet_image_url,
# pet_name, pet_profile_image1, pet_profile_image2, pet_profile_image3,
# shelterRegisterData, shelterRegisterData_id
class Pet(models.Model):
    shelterRegisterData = models.ForeignKey(
        ShelterRegisterData, null=True, on_delete=models.CASCADE, related_name="pet"
    )
    favorite = models.ManyToManyField(User, related_name="favorite", blank=True)
    pet_name = models.CharField(max_length=80)
    pet_breed = models.CharField(max_length=50)
    pet_age = models.CharField(max_length=10)
    pet_color = models.CharField(max_length=50)
    pet_gender = models.CharField(max_length=50)
    pet_adoption_status = models.BooleanField("Is Adopted", default=False)
    pet_pending_status = models.BooleanField("Is Adoption pending", default=False)
    pet_pending_user = models.ManyToManyField(
        User, related_name="Pending_User", blank=True
    )
    pet_profile_image1 = models.ImageField(
        default="default.jpg", upload_to="pet_profile_pics", blank=True
    )
    pet_image_url = models.URLField(
        max_length=250,
        blank=True,
        default="https://dl5zpyw5k3jeb.cloudfront.net/photos/pets/48212723/1/?bust=1592050579&width=450",
    )
    pet_profile_image2 = models.ImageField(
        default="default.jpg", upload_to="pet_profile_pics", blank=True
    )
    pet_profile_image3 = models.ImageField(
        default="default.jpg", upload_to="pet_profile_pics", blank=True
    )

    def __str__(self):
        return self.pet_name

    # the below method will captilize the fist letter of the below listed fields
    # when they are entered. This is important for the column sorting to work.
    def save(self, *args, **kwargs):
        for field_name in [
            "pet_name",
            "pet_breed",
            "pet_color",
            "pet_gender",
        ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Pet, self).save(*args, **kwargs)

        img = Image.open(self.pet_profile_image1.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pet_profile_image1.path)

        img = Image.open(self.pet_profile_image2.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pet_profile_image2.path)

        img = Image.open(self.pet_profile_image3.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.pet_profile_image3.path)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="to_user"
    )
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user=from_user, sender=from_user, recipient=to_user, body=body, is_read=True
        )

        sender_message.save()

        recipient_message = Message(
            user=to_user,
            sender=from_user,
            recipient=from_user,
            body=body,
        )

        recipient_message.save()

        return sender_message

    def get_messages(user):
        users = []
        messages = (
            Message.objects.filter(user=user)
            .values("recipient")
            .annotate(last=Max("date"))
            .order_by("-last")
        )
        for message in messages:
            users.append(
                {
                    "user": User.objects.get(pk=message["recipient"]),
                    "last": message["last"],
                    "unread": Message.objects.filter(
                        user=user, recipient__pk=message["recipient"], is_read=False
                    ).count(),
                }
            )
        return users
