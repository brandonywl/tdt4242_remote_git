"""
Tests for the workouts application.
"""
from django.test import TestCase
from users.serializers import UserSerializer

from users.models import User
# Create your tests here.

class UserSerializerTest(TestCase):
    def setUp(self):
        self.data = {
            "username": "admin",
            "email": "wlyeow@stud.ntnu.no",
            "password": "12345678",
            "phone_number": 12345678,
            "country": "Norway",
            "city": "Trondheim",
            "street_address": "123 Happy Lane",
            "password1": "12345678"
        }

        self.user = User.objects.create()


    def test_validate_password(self):
        serializer = UserSerializer.create(self.user, validated_data=self.data)
        print(serializer)
        print(dir(serializer))
        self.assertEqual(serializer.validate_password(0), 0)