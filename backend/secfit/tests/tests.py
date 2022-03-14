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
            "unit": "reps",
            "video": "https://www.youtube.com/embed/IODxDxX7oi4",
            "owner_name": self.user_payload["username"]
        }

        self.create_user()
        self.login_user()
        self.create_exercise()
        # self.edit_exercise()

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

        payload = {
            "name": "Push-up",
            "description": "A push-up (or press-up in British English) is a common calisthenics exercise beginning from the prone position.",
            "unit": "reps",
            "video": "https://www.youtube.com/embed/IODxDxX7oi4",
            "owner": self.user["url"],
            "owner_name": self.user["username"],
        }

        response = self.client.post(api, payload)
        self.assertTrue(response.status_code, 201)

    def edit_exercise(self, payload, id=1):
        api = f'api/exercises/{id}/'
        response = self.client.post(api, payload)
        return response

    def test_test(self):
        # self.login_user()
        # self.edit_exercise()
        # print(self.data)
        pass