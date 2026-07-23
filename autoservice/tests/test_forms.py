from django.test import TestCase

from autoservice.forms import OrderForm
from autoservice.models import OrderType


class TestOrderCreate(TestCase):
    def setUp(self):
        self.order_types = OrderType.objects.create(
            name="testOrderType",
        )

    def test_order_form_missing_required_fields(self):
        form_data = {
            "client_full_name": "Sara Stoun",
            "client_number": "12345756",
            "car_model": "Tesla 3",
            "car_year": "2020",
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("order_types", form.errors)

    def test_create_order_with_required_fields(self):
        form_data = {
            "client_full_name": "Sara Stoun",
            "client_number": "12345756",
            "car_model": "Tesla 3",
            "car_year": "2020",
            "order_types": [self.order_types.id],
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())