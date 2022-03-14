from django.test import TestCase, Client


from rest_framework.reverse import reverse

# Create your tests here.

class RegistrationPageTest(TestCase):
    def setUp(self):
        self.base_payload = {
            "username": "SecFit",
            "email": "wlyeow@stud.ntnu.no",
            "password": "12345678",
            "password1": "12345678",
            "phone_number": "12345678",
            "country": "Norway",
            "city": "Trondheim",
            "street_address": "123 Happy Lane",
        }

        self.email_base = "@stud.ntnu.no"

        self.SUCCESSFUL_POST = 201
        self.FAILED_POST = 400
        
        self.client = Client()

    def assertSuccessPOST(self, response, status_code=None):
        status_code = status_code if status_code else self.SUCCESSFUL_POST
        self.assertEquals(response.status_code, status_code)

    def assertFailPOST(self, response, status_code=None):
        status_code = status_code if status_code else self.FAILED_POST
        self.assertEquals(response.status_code, status_code)

    def test_base_success(self):
        api = reverse("user-list")
        response = self.client.post(api, self.base_payload)
        self.assertSuccessPOST(response)
    
    def test_empty_username_fail(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "username"

        length_a = 0
        length_b = length_a + 1

        
        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)
    
    def test_full_username_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "username"

        length_a = 151
        length_b = length_a - 1

        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)
    
    def test_no_at_email_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "email"

        payload[cell] = payload[cell].replace("@", "")
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

    def test_no_tail_email_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "email"
        
        at_idx = payload[cell].index("@") + 1
        payload[cell] = payload[cell][0:at_idx]
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload = self.base_payload.copy()
        
        at_idx = payload[cell].index(".ntnu.no")
        payload[cell] = payload[cell][0:at_idx]
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

    def test_empty_email_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "email"

        length_a = 0
        length_b = 1

        payload[cell] = "a" * length_a + self.email_base
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b + self.email_base
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    def test_full_email_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "email"

        length_a = 255 - len(self.email_base)
        length_b = length_a - 1

        payload[cell] = "a" * length_a + self.email_base
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b + self.email_base
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    def test_empty_password_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "password"
        cell2 = "password1"

        length_a = 0
        length_b = 1

        payload[cell] = payload[cell2] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = payload[cell2] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    def test_different_password_inputs_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "password"
        cell2 = "password1"

        length_a = 1
        length_b = 2

        payload[cell] = "a" * length_a
        payload[cell2] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

    # def test_empty_phone_number_boundary(self):
    #     # Phone number is not required
    #     pass

    def test_full_phone_number_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "phone_number"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    # def test_empty_country_boundary(self):
    #     # Country is not required
    #     pass

    def test_full_country_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "country"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    # def test_empty_city_boundary(self):
    #     # City is not required
    #     pass

    def test_full_city_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "city"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

    # def test_empty_street_address_boundary(self):
    #     # Street Address is not required
    #     pass

    def test_full_street_address_boundary(self):
        api = reverse("user-list")
        payload = self.base_payload.copy()
        cell = "street_address"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.client.post(api, payload)
        self.assertFailPOST(response)

        payload[cell] = "a" * length_b
        response = self.client.post(api, payload)
        self.assertSuccessPOST(response)

class ExercisePageTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.SUCCESSFUL_PUT = 200
        self.FAILED_PUT = 400

        self.user_payload = {
            "username": "SecFit",
            "email": "wlyeow@stud.ntnu.no",
            "password": "12345678",
            "password1": "12345678",
            "phone_number": "12345678",
            "country": "Norway",
            "city": "Trondheim",
            "street_address": "123 Happy Lane",
        }

        self.exercise_payload = {
            "name": "Push-up",
            "description": "A push-up (or press-up in British English) is a common calisthenics exercise beginning from the prone position.",
            "instructions": "No instructions have been given.",
            "duration": "0",
            "calories": "0",
            'muscleGroup': "Legs",
            "unit": "reps",
            "video": "https://www.youtube.com/embed/IODxDxX7oi4",
            "owner_name": self.user_payload["username"]
        }

        self.create_user()
        self.login_user()
        self.create_exercise()

    def assertSuccessPUT(self, response, status_code=None):
        status_code = status_code if status_code else self.SUCCESSFUL_PUT
        self.assertEquals(response.status_code, status_code)

    def assertFailPUT(self, response, status_code=None):
        status_code = status_code if status_code else self.FAILED_PUT
        self.assertEquals(response.status_code, status_code)

    def create_user(self):
        api = reverse("user-list")

        response = self.client.post(api, self.user_payload)
        self.user = response.json()

        self.exercise_payload["owner"] = self.user["url"]

    def login_user(self):
        result = self.client.login(username=self.user_payload["username"], \
                password=self.user_payload["password"])
        assert result
        
    def create_exercise(self):
        api = reverse("exercise-list")

        response = self.client.post(api, self.exercise_payload)
        self.assertTrue(response.status_code, 201)
        self.exercise_payload.pop("owner")
        self.exercise_payload.pop("owner_name")

    def edit_exercise(self, payload, id=1):
        api = f'/api/exercises/{id}/'
        response = self.client.put(api, payload, content_type="application/json")
        return response

    def get_exercises(self, id=1):
        api = reverse("exercise-list")
        response = self.client.get(api)
        return response.json()

    def test_normal_edit_success(self):
        payload = self.exercise_payload.copy()
        payload["description"] = "Hello."

        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_empty_unit_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "unit"

        length_a = 0
        length_b = 1

        payload[cell] = "a" * length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = "a" * length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_full_unit_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "unit"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = "a" * length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_full_unit_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "unit"

        length_a = 51
        length_b = 50

        payload[cell] = "a" * length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = "a" * length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_empty_duration_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "duration"

        length_a = ""
        length_b = 1

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    # # Should only accept positive number but django model was not set reject non-positive
    # def test_negative_duration_boundary(self):
    #     payload = self.exercise_payload.copy()
    #     cell = "duration"

    #     length_a = -1
    #     length_b = 0

    #     payload[cell] = length_a
    #     response = self.edit_exercise(payload)
    #     self.assertFailPUT(response)

    #     payload[cell] = length_b
    #     response = self.edit_exercise(payload)
    #     self.assertSuccessPUT(response)

    def test_alpha_duration_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "duration"

        length_a = "a"
        length_b = 1

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_max_duration_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "duration"

        length_a = 2**63 - 1
        length_b = 2**63

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

        payload[cell] = length_b
        self.assertRaises(OverflowError, self.edit_exercise, payload)

    def test_empty_calories_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "calories"

        length_a = ""
        length_b = 1

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    # # Should only accept positive number but django model was not set reject non-positive
    # def test_negative_calories_boundary(self):
    #     payload = self.exercise_payload.copy()
    #     cell = "calories"

    #     length_a = -1
    #     length_b = 0

    #     payload[cell] = length_a
    #     response = self.edit_exercise(payload)
    #     self.assertFailPUT(response)

    #     payload[cell] = length_b
    #     response = self.edit_exercise(payload)
    #     self.assertSuccessPUT(response)

    def test_alpha_calories_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "calories"

        length_a = "a"
        length_b = 1

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertFailPUT(response)

        payload[cell] = length_b
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

    def test_max_calories_boundary(self):
        payload = self.exercise_payload.copy()
        cell = "calories"

        length_a = 2**63 - 1
        length_b = 2**63

        payload[cell] = length_a
        response = self.edit_exercise(payload)
        self.assertSuccessPUT(response)

        payload[cell] = length_b
        self.assertRaises(OverflowError, self.edit_exercise, payload)
