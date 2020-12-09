from django.db import models
from PIL import Image
from accounts.models import UserRegisterData


# ClientUserPet has fields id, pet_age, pet_breed, pet_color, pet_gender, pet_image_url,
# pet_name, pet_profile_image1, pet_profile_image2, pet_profile_image3,
# shelterRegisterData, shelterRegisterData_id
class ClientUserPet(models.Model):
    userRegisterData = models.ForeignKey(
        UserRegisterData, null=True, on_delete=models.CASCADE, related_name="pet"
    )
    pet_name = models.CharField(max_length=80)
    pet_breed = models.CharField(max_length=50)
    pet_age = models.CharField(max_length=10)
    pet_color = models.CharField(max_length=50)
    pet_gender = models.CharField(max_length=50)
    pet_spayneuter = models.CharField(max_length=50, default="Yes")
    pet_playdate_day1 = models.CharField(max_length=50, default="Friday")
    pet_playdate_time1 = models.CharField(max_length=50, default="Night")
    pet_profile_image1 = models.ImageField(
        default="default.jpg", upload_to="pet_profile_pics", blank=True
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
        super(ClientUserPet, self).save(*args, **kwargs)

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
