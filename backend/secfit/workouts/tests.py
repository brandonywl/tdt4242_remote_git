"""
Tests for the workouts application.
"""
from django.test import TestCase, Client

from users.models import User
from workouts.models import Workout

from workouts.permissions import IsOwner, CanEdit, IsOwnerOfWorkout, \
    IsCoachAndVisibleToCoach, IsCoachOfWorkoutAndVisibleToCoach, IsPublic, \
    IsWorkoutPublic, IsReadOnly

from datetime import datetime
from django.utils.timezone import make_aware

# Create your tests here.

class StubUser():
    def __init__(self, owner, coach=None):
        self.owner = owner
        self.coach = coach

class StubRequest():
    def __init__(self, user, methodtype, data=None):
        self.user = user
        self.method = methodtype
        self.data = data

class StubWorkout():
    def __init__(self, visibility, owner):
        self.visibility = visibility
        self.owner = owner

class StubObj():
    def __init__(self, workout=None, owner=None):
        self.workout=workout
        self.owner=owner


class OwnerPermissionTest(TestCase):
    def setUp(self):
        self.owner = StubUser("SecFit")
        self.request = StubRequest("SecFit", "GET")
        self.different_user_request = StubRequest("George", "GET")
        
        self.permission = IsOwner()

    def test_is_owner_success(self):
        perm = self.permission.has_object_permission(obj=self.owner, request=self.request, view=None)
        self.assertTrue(perm, "Issue where obj.owner != request.user when it should be")

    def test_is_owner_fail(self):
        perm = self.permission.has_object_permission(obj=self.owner, request=self.different_user_request, view=None)
        self.assertFalse(perm, "Issue where obj.owner == request.user when it should not")


class CanEditPermissionTest(TestCase):
    def setUp(self):
        self.owner = StubUser("SecFit")
        self.get_request = StubRequest("SecFit", "GET")
        self.post_request = StubRequest("SecFit", "PUT")
        self.user_get_request = StubRequest("George", "GET")
        self.user_post_request = StubRequest("George", "PUT")
        
        self.permission = CanEdit()

    def test_get_request_success(self):
        perm = self.permission.has_object_permission(self.get_request, None, self.owner)
        self.assertTrue(perm)
        perm = self.permission.has_object_permission(self.user_get_request, None, self.owner)
        self.assertTrue(perm)

    def test_post_request_success(self):
        perm = self.permission.has_object_permission(self.post_request, None, self.owner)
        self.assertTrue(perm)

    def test_post_request_fail(self):
        perm = self.permission.has_object_permission(self.user_post_request, None, self.owner)
        self.assertFalse(perm)


class IsOwnerWorkoutPermissionTest(TestCase):
    def setUp(self):
        self.url = "api/workouts/1/"
        self.data = {"workout": self.url}
        self.wrong_data = {"exercise": self.url.replace("workouts", "exercises")}

        self.user = User.objects.create(username="SecFit", password="unitTest123")
        self.user2 = User.objects.create(username="Fred", password="unitTest123")
        date = make_aware(datetime(2022, 4, 8, 23, 55, 59, 342380))
        self.workout = Workout.objects.create(name="Test", date=date, notes="Test", owner=self.user)

        self.correct_post_request = StubRequest(self.user, "POST", self.data)
        self.wrong_post_request = StubRequest(self.user2, "POST", self.data)
        self.wrong_data_post_request = StubRequest(self.user, "POST", self.wrong_data)
        self.self_get_request = StubRequest(self.user, "GET", self.data)
        self.get_request = StubRequest(self.user2, "GET", self.data)

        self.workout_obj = StubObj(self.workout)

        self.permission = IsOwnerOfWorkout()

    def test_post_success(self):
        perm = self.permission.has_permission(self.correct_post_request, "")
        self.assertTrue(perm)

    def test_post_fail(self):
        perm = self.permission.has_permission(self.wrong_post_request, "")
        self.assertFalse(perm)

    def test_wrong_data_post_fail(self):
        perm = self.permission.has_permission(self.wrong_data_post_request, "")
        self.assertFalse(perm)

    def test_get_success(self):
        perm = self.permission.has_permission(self.get_request, "")
        self.assertTrue(perm)
        perm = self.permission.has_permission(self.self_get_request, "")
        self.assertTrue(perm)

    def test_obj_success(self):
        perm = self.permission.has_object_permission(self.correct_post_request, "", self.workout_obj)
        self.assertTrue(perm)

    def test_obj_fail(self):
        perm = self.permission.has_object_permission(self.wrong_post_request, "", self.workout_obj)
        self.assertFalse(perm)


class IsCoachAndCoachVizPermissionTest(TestCase):
    def setUp(self):
        self.coach = StubUser("SecFit")
        self.user = StubUser("George", self.coach)
        self.request = StubRequest(self.coach, "GET")
        self.second_user = StubUser("Fred")
        self.second_request = StubRequest(self.second_user, "GET")
        self.workout = StubWorkout("PU", self.user)

        self.permission = IsCoachAndVisibleToCoach()

    def test_coach_and_visible_success(self):
        perm = self.permission.has_object_permission(self.request, "", self.workout)
        self.assertTrue(perm)

    def test_not_coach_fail(self):
        perm = self.permission.has_object_permission(self.second_request, "", self.workout)
        self.assertFalse(perm)



class IsCoachWorkoutAndCoachVizPermissionTest(TestCase):
    def setUp(self):
        self.coach = StubUser("SecFit")
        self.user = StubUser("George", self.coach)
        self.request = StubRequest(self.coach, "GET")
        self.second_user = StubUser("Fred")
        self.second_request = StubRequest(self.second_user, "GET")
        self.workout = StubWorkout("PU", self.user)
        self.workout_obj = StubObj(self.workout, self.user)

        self.permission = IsCoachOfWorkoutAndVisibleToCoach()

    def test_coach_and_visible_success(self):
        perm = self.permission.has_object_permission(self.request, "", self.workout_obj)
        self.assertTrue(perm)

    def test_not_coach_fail(self):
        perm = self.permission.has_object_permission(self.second_request, "", self.workout_obj)
        self.assertFalse(perm)


class IsPublicPermissionTest(TestCase):
    def setUp(self):
        self.public_workout = StubWorkout("PU", None)
        self.coach_workout = StubWorkout("CO", None)
        self.private_workout = StubWorkout("PR", None)

        self.permission = IsPublic()

    def test_public_workout_success(self):
        perm = self.permission.has_object_permission("", "", self.public_workout)
        self.assertTrue(perm)

    def test_public_workout_fail(self):
        perm = self.permission.has_object_permission("", "", self.coach_workout)
        self.assertFalse(perm)
        perm = self.permission.has_object_permission("", "", self.private_workout)
        self.assertFalse(perm)


class IsWorkoutPublicPermissionTest(TestCase):
    def setUp(self):
        public_workout = StubWorkout("PU", None)
        coach_workout = StubWorkout("CO", None)
        private_workout = StubWorkout("PR", None)

        
        self.public_workout_obj = StubObj(public_workout, None)
        self.coach_workout_obj = StubObj(coach_workout, None)
        self.private_workout_obj = StubObj(private_workout, None)
    
        self.permission = IsWorkoutPublic()

    def test_public_workout_success(self):
        perm = self.permission.has_object_permission("", "", self.public_workout_obj)
        self.assertTrue(perm)

    def test_public_workout_fail(self):
        perm = self.permission.has_object_permission("", "", self.coach_workout_obj)
        self.assertFalse(perm)
        perm = self.permission.has_object_permission("", "", self.private_workout_obj)
        self.assertFalse(perm)


class IsReadOnlyPermissionTest(TestCase):
    def setUp(self):
        self.get_request = StubRequest("SecFit", "GET")
        self.head_request = StubRequest("SecFit", "HEAD")
        self.post_request = StubRequest("SecFit", "POST")
        self.put_request = StubRequest("SecFit", "PUT")

        self.permission = IsReadOnly()

    def test_safe_requests_success(self):
        self.assertTrue(self.permission.has_object_permission(self.get_request, "", ""))
        self.assertTrue(self.permission.has_object_permission(self.head_request, "", ""))

    def test_safe_requests_fail(self):
        self.assertFalse(self.permission.has_object_permission(self.put_request, "", ""))
        self.assertFalse(self.permission.has_object_permission(self.post_request, "", ""))
