from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

ORDER_URL = reverse("autoservice:order-list")
LOGIN_URL = reverse("login")


class PublicOrderTest(TestCase):
    def test_login_required_redirect(self):
        response = self.client.get(ORDER_URL)
        expected_url = f"{LOGIN_URL}?next={ORDER_URL}"
        self.assertRedirects(response, expected_url)


class PrivateOrderTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="1qwer2rewq",
        )
        self.client.force_login(self.user)

    def test_service_advisor_successful_enter_the_page(self):
        response = self.client.get(ORDER_URL)
        self.assertEqual(response.status_code, 200)

    def test_404_error_for_non_existent_order(self):
        url = reverse("autoservice:order-detail", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
