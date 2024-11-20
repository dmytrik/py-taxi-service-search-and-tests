from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Manufacturer, Car


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="bmw",
            country="germany"
        )
        self.driver_data = {
            "username": "test_new_user",
            "password1": "test_password1",
            "password2": "test_password1",
            "license_number": "ABC12345",
            "first_name": "test_first_test",
            "last_name": "test_last_test",
        }
        self.manufacturer_data = {
            "name": "bmw",
            "country": "germany"
        }
        self.car_data = {
            "model": "x5",
            "manufacturer": self.manufacturer,
            "drivers": [self.user]
        }
        self.client.force_login(self.user)

    def test_driver_creation_form_with_license_number_is_valid(self):
        form = DriverCreationForm(data=self.driver_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.driver_data)

    def test_create_driver(self):
        self.client.post(reverse("taxi:driver-create"), data=self.driver_data)
        new_user = get_user_model().objects.get(
            username=self.driver_data["username"]
        )

        self.assertEqual(new_user.first_name, self.driver_data["first_name"])
        self.assertEqual(new_user.last_name, self.driver_data["last_name"])
        self.assertEqual(
            new_user.license_number,
            self.driver_data["license_number"]
        )

    def test_car_creation_form(self):
        form = CarForm(data=self.car_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["model"],
            self.car_data["model"]
        )
        self.assertEqual(
            form.cleaned_data["manufacturer"],
            self.car_data["manufacturer"]
        )

    def test_create_manufacturer(self):
        self.client.post(
            reverse("taxi:manufacturer-create"),
            data=self.manufacturer_data
        )
        new_manufacturer = Manufacturer.objects.get(
            name=self.manufacturer_data["name"]
        )

        self.assertEqual(
            new_manufacturer.name,
            self.manufacturer_data["name"]
        )
        self.assertEqual(
            new_manufacturer.country,
            self.manufacturer_data["country"]
        )
