from django.test import TestCase
from django.urls import reverse

from autoservice.models import (
    ServiceAdvisor,
    Technician,
    MasterQualification,
    Order,
    OrderType
)


class TestModels(TestCase):
    def setUp(self):
        self.order_types = OrderType.objects.create(
            name="testOrderType",
        )
        self.master_qualification = MasterQualification.objects.create(
            name="testMasterQualification",
        )
        self.technician1 = Technician.objects.create(
            first_name="testFirstName",
            last_name="testLastName",
            master_qualification=self.master_qualification,
        )
        self.technician2 = Technician.objects.create(
            first_name="testFirstName2",
            last_name="testLastName2",
            master_qualification=self.master_qualification,
        )
        self.technician3 = Technician.objects.create(
            first_name="testFirstName3",
            last_name="testLastName3",
            master_qualification=self.master_qualification,
        )

        self.service_advisor = ServiceAdvisor.objects.create(
            username="testUser",
            first_name="testFirstName",
            last_name="testLastName",
            password="1qawsed32",
        )

        self.order1 = Order.objects.create(
            client_full_name="testClientFullName",
            client_number="3714545372",
            car_model="testCarModel",
            car_year="2027",
            service_advisor=self.service_advisor,
        )
        self.order1.order_types.add(self.order_types)

        self.order2 = Order.objects.create(
            client_full_name="testClientFullName2",
            client_number="3714545373",
            car_model="testCarModel1",
            car_year="2026",
            service_advisor=self.service_advisor,
        )

        self.order3 = Order.objects.create(
            client_full_name="testClientFullName3",
            client_number="3714545371",
            car_model="testCarModel5",
            car_year="2023",
            service_advisor=self.service_advisor,
            is_archived=True,
        )
        self.client.force_login(self.service_advisor)

    def test_active_orders_count(self):
        self.assertEqual(self.service_advisor.active_orders_count, 2)

    def test_technician_many_to_many_assignment(self):
        self.order1.technicians.add(self.technician1, self.technician2)
        self.assertEqual(self.order1.technicians.count(), 2)

    def test_service_advisor_str_return_correct_format(self):
        self.assertEqual(
            str(self.service_advisor),
            f"{self.service_advisor.username} "
            f"({self.service_advisor.first_name} "
            f"{self.service_advisor.last_name})"
        )

    def test_technician_str_return_correct_format(self):
        self.assertEqual(
            str(self.technician1),
            (f"{self.technician1.first_name} {self.technician1.last_name}"
             f" ({self.technician1.master_qualification})"
             )
        )

    def test_order_str_return_correct_format(self):
        self.assertEqual(
            str(self.order3),
            (f"{self.order3.created_at} {self.order3.car_model}"
             f" {self.order3.car_year} {self.order3.client_full_name}"
             f" {self.order3.client_number}"
             )
        )

    def test_active_orders_count_distinct(self):
        self.order1.technicians.add(
            self.technician1,
            self.technician2,
            self.technician3
        )
        response = self.client.get(reverse("autoservice:index"))
        self.assertEqual(response.context["active_orders_count"], 1)

    def test_assign_manager_to_order(self):
        self.order1.service_advisor = None
        self.order1.save()
        toggle_url = reverse(
            "autoservice:toggle-order-assign",
            args=[self.order1.id]
        )
        self.client.get(toggle_url)
        self.order1.refresh_from_db()
        self.assertEqual(self.order1.service_advisor, self.service_advisor)

    def test_remove_service_advisor_from_order(self):
        toggle_url = reverse(
            "autoservice:toggle-order-assign",
            args=[self.order1.id]
        )
        self.client.get(toggle_url)
        self.order1.refresh_from_db()
        self.assertIsNone(self.order1.service_advisor)

    def test_archive_order(self):
        archive_url = reverse(
            "autoservice:order-delete",
            args=[self.order2.id]
        )
        self.client.post(archive_url)
        self.order2.refresh_from_db()
        self.assertTrue(self.order2.is_archived)
        self.assertTrue(Order.objects.filter(id=self.order2.id).exists())

    def test_restore_order_from_archive(self):
        restore_url = reverse(
            "autoservice:order-restore",
            args=[self.order3.id]
        )
        self.client.post(restore_url)
        self.order3.refresh_from_db()
        self.assertFalse(self.order3.is_archived)
