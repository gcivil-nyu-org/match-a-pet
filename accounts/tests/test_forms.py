from django.test import SimpleTestCase, TestCase
from accounts.forms import (
    ShelterRegistrationForm,
    ShelterUserUpdateForm,
    ShelterUpdateForm,
    PetForm,
    # UserRegistrationForm,
    ClientUserUpdateForm,
    ClientUpdateForm,
)


class DefaultTestFroms(TestCase):
    # ** Testing ShelterRegistrationForm
    def test_ShelterRegistrationForm_valid(self):
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
                "zip_code": "12189",
                "password1": "test123abc",
                "password2": "test123abc",
            }
        )

        self.assertTrue(form.is_valid())

    def test_ShelterRegistrationForm_no_data(self):
        form = ShelterRegistrationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 11)

    def test_ShelterRegistrationForm_invalid_data(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 10)

    def test_ShelterRegistrationForm_invalid_data1(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "12189",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_ShelterRegistrationForm_invalid_data2(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "city": "Manhattan",
                "state": "ny",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_ShelterRegistrationForm_invalid_data3(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "city": "Manhattan",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_ShelterRegistrationForm_invalid_data4(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

    def test_ShelterRegistrationForm_invalid_data5(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 8)

    def test_ShelterRegistrationForm_invalid_data6(self):
        form = ShelterRegistrationForm(
            data={
                "username": "peter7",
                "email": "peter@matchapet.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 9)

    def test_ShelterRegistrationForm_invalid_data7(self):
        form = ShelterRegistrationForm(
            data={
                "email": "peter@matchapet.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 10)

    # ** Testing ShelterUserUpdateForm
    def test_ShelterUserUpdateForm_valid(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "address": "5th Ave",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "12189",
            }
        )

        self.assertTrue(form.is_valid())

    def test_ShelterUserUpdateForm_no_data(self):
        form = ShelterUserUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

    def test_ShelterUserUpdateForm_invalid_data(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_ShelterUserUpdateForm_invalid_data1(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_ShelterUserUpdateForm_valid2(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_ShelterUserUpdateForm_valid3(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "city": "Brooklyn",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_ShelterUserUpdateForm_valid4(self):
        form = ShelterUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # ** Testing ShelterUpdateForm
    def test_ShelterUpdateForm_valid(self):
        form = ShelterUpdateForm(data={"shelter_profile_image": "default.jpg"})

        self.assertTrue(form.is_valid())

    # # ** Testing UserRegistrationForm
    # def test_UserRegistrationForm_valid(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #             "last_name": "Voltz",
    #             "address": "5th Ave",
    #             "city": "Manhattan",
    #             "state": "ny",
    #             "zip_code": "12189",
    #             "password1": "test123abc",
    #             "password2": "test123abc",
    #         }
    #     )
    #
    #     self.assertTrue(form.is_valid())
    #
    # def test_UserRegistrationForm_no_data(self):
    #     form = UserRegistrationForm(data={})
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 10)
    #
    # def test_UserRegistrationForm_invalid_data(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 9)
    #
    # def test_SUserRegistrationForm_invalid_data1(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #             "last_name": "Voltz",
    #             "city": "Manhattan",
    #             "state": "ny",
    #             "password1": "test123abc",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 3)
    #
    # def test_UserRegistrationForm_invalid_data2(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #             "last_name": "Voltz",
    #             "city": "Manhattan",
    #             "state": "ny",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 4)
    #
    # def test_UserRegistrationForm_invalid_data3(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #             "last_name": "Voltz",
    #             "city": "Manhattan",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 5)
    #
    # def test_UserRegistrationForm_invalid_data4(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #             "last_name": "Voltz",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 6)
    #
    # def test_UserRegistrationForm_invalid_data5(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #             "first_name": "Peter",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 7)
    #
    # def test_UserRegistrationForm_invalid_data6(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "username": "peter7",
    #             "email": "peter@matchapet.com",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 8)
    #
    # def test_UserRegistrationForm_invalid_data7(self):
    #     form = UserRegistrationForm(
    #         data={
    #             "email": "peter@matchapet.com",
    #         }
    #     )
    #
    #     self.assertFalse(form.is_valid())
    #     self.assertEquals(len(form.errors), 9)

    # ** Testing ClientUserUpdateForm
    def test_ClientUserUpdateForm_valid(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "address": "5th Ave",
                "city": "Manhattan",
                "state": "ny",
                "zip_code": "12189",
            }
        )

        self.assertTrue(form.is_valid())

    def test_ClientUserUpdateForm_no_data(self):
        form = ClientUserUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

    def test_ClientUserUpdateForm_invalid_data(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_ClientUserUpdateForm_invalid_data1(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_ClientUserUpdateForm_valid2(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_ClientUserUpdateForm_valid3(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
                "city": "Brooklyn",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_ClientUserUpdateForm_valid4(self):
        form = ClientUserUpdateForm(
            data={
                "username": "peter3",
                "email": "peter@matchapet.com",
                "first_name": "Peter",
                "last_name": "Voltz",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # ** Testing ClientUpdateForm
    def test_ClientUpdateForm_valid(self):
        form = ClientUpdateForm(data={"user_profile_image": "default.jpg"})

        self.assertTrue(form.is_valid())


class TestForms(SimpleTestCase):
    def test_PetForm_valid(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
                "pet_breed": "Dog",
                "pet_age": "Baby",
                "pet_color": "White",
                "pet_gender": "Female",
            }
        )

        self.assertTrue(form.is_valid())

    def test_PetForm_no_data(self):
        form = PetForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_PetForm_invalid_data(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
                "pet_breed": "Dog",
                "pet_age": "4",
                "pet_color": "White",
                "pet_gender": "Female",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_PetForm_invalid_data1(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
                "pet_breed": "Dog",
                "pet_age": "4",
                "pet_color": "White",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_PetForm_invalid_data2(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
                "pet_breed": "Dog",
                "pet_age": "4",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_PetForm_invalid_data3(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
                "pet_breed": "Dog",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_PetForm_invalid_data4(self):
        form = PetForm(
            data={
                "pet_name": "Sheila",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)


# ******
