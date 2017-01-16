from django.urls.exceptions import NoReverseMatch
from django.test import TestCase
from django.test import Client
from drawer.models import Value
from drawer.models import Token
from django.urls import reverse


class APITest(TestCase):
    def setUp(self):
        self.client = Client()

    def get_token_dict(self):
        if self.token:
            return {"token": self.token}
        else:
            raise Exception("No token set!")

    def register_new_user(self):
        # Set up super-simple auth
        resp = self.client.post(reverse("drawer:register"))
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, "token")
        self.token = resp.json().get("token")

    def store_key_value(self, key, value):
        resp = self.client.post(reverse(
            "drawer:store", kwargs={
                "key": key, "value": value}
        ), data=self.get_token_dict())
        self.assertEquals(resp.status_code, 200)

    def test_store_new_value_no_token(self):
        # Forget super-simple auth
        self.register_new_user()
        resp = self.client.post(reverse(
            "drawer:store", kwargs={
                "key": "TEST_KEY", "value": "TEST_VALUE"}))
        self.assertEquals(resp.status_code, 403)

    def test_store_new_value_token(self):
        # Use super-simple auth
        self.register_new_user()
        resp = self.client.post(reverse(
            "drawer:store", kwargs={
                "key": "TEST_KEY", "value": "TEST_VALUE"}
        ), data=self.get_token_dict())
        self.assertEquals(resp.status_code, 200)

    def test_store_and_retrieve_token(self):
        # Use super-simple auth
        TEST_KEY = "TEST_KEY"
        TEST_VALUE = "TEST_VALUE"
        self.register_new_user()
        resp = self.client.post(reverse(
            "drawer:store", kwargs={
                "key": TEST_KEY, "value": TEST_VALUE}
        ), data={"token": self.token})
        self.assertEquals(resp.status_code, 200)

        resp = self.client.post(reverse(
            "drawer:retrieve",
            kwargs={"key": TEST_KEY}),
            data=self.get_token_dict())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json().get("TEST_KEY"), TEST_VALUE)

    def test_store_failures(self):
        # Key too long
        TEST_KEY = "tooolongkeynamevaluestorethrowanerror"
        TEST_VALUE = "TEST_VALUE"
        self.register_new_user()
        with self.assertRaises(NoReverseMatch):
            reverse(
                "drawer:store", kwargs={
                    "key": TEST_KEY, "value": TEST_VALUE}
            )

        resp = self.client.post(
            "store/{}/{}/".format(TEST_KEY,
                                  TEST_VALUE), data=self.get_token_dict())
        self.assertEquals(resp.status_code, 404)

    def test_retrieve_token_fail(self):
        # No token
        TEST_KEY = "TEST_KEY"
        self.register_new_user()
        resp = self.client.post(reverse(
            "drawer:retrieve",
            kwargs={"key": TEST_KEY}),
            data=self.get_token_dict())
        self.assertEquals(resp.status_code, 400)

    def test_retrieve_all_empty(self):
        # Get all, no values
        self.register_new_user()
        resp = self.client.post(reverse("drawer:retrieve_all"),
                                data=self.get_token_dict())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json(), [])

    def test_retrieve_all(self):
        self.register_new_user()
        self.store_key_value("TEST", "VALUE")
        self.store_key_value("TEST_2", "VALUE_2")
        resp = self.client.post(reverse("drawer:retrieve_all"),
                                data=self.get_token_dict())
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, "VALUE")
        self.assertContains(resp, "TEST")

    def test_just_register(self):
        self.register_new_user()  # Hidden in util function

    def tearDown(self):
        Token.objects.all().delete()
        Value.objects.all().delete()
