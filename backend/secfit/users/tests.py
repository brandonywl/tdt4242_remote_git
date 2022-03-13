"""
Tests for the users application.
"""
from django.test import TestCase
from django.forms.models import model_to_dict
from users.serializers import UserSerializer
from rest_framework import serializers

from users.models import User
# Create your tests here.

class UserSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "admin",
            "email": "wlyeow@stud.ntnu.no",
            "password": "12345678",
            "phone_number": "12345678",
            "country": "Norway",
            "city": "Trondheim",
            "street_address": "123 Happy Lane",
            "password1": "12345678"
        }

        self.bad_data = self.data.copy()
        self.bad_data["password1"] = "abcdefgh"


    def test_validate_password_success(self):
        value = 0

        serializer = UserSerializer(data=self.data)
        result = UserSerializer.validate_password(serializer, value)

        self.assertEquals(value, result)

    def test_validate_password_fail(self):
        value = 0

        serializer = UserSerializer(data=self.bad_data)
        self.assertRaises(serializers.ValidationError, serializer.validate_password, value)

    def test_create_user(self):
        franky_data = self.data.copy()
        franky_data["username"] = "franky"

        serializer = UserSerializer(data=franky_data)
        user = serializer.create(franky_data)
        franky = User.objects.get(username="franky")

        self.assertEquals(user, franky) # Assert that it is successfully stored in db

        self.assertTrue(franky.check_password(franky_data["password"])) # Assert that password is stored properly

        model_dict = model_to_dict(franky)
        franky_dict = franky_data.copy()
        franky_dict.pop("password")
        franky_dict.pop("password1")

        # Assert that all values are stored properly
        for key, value in franky_dict.items():
            self.assertEquals(model_dict[key], value)
