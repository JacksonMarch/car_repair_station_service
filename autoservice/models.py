from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class MasterQualification(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class OrderType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ServiceAdvisor(AbstractUser):

    class Meta:
        ordering = ["username"]


    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("autoservice:service-advisor-detail", kwargs={"pk": self.pk})


class Technician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    master_qualification = models.ForeignKey(MasterQualification, on_delete=models.CASCADE)
    experience = models.TextField(blank=True)

    class Meta:
        ordering = ["master_qualification"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.master_qualification})"

    def get_absolute_url(self):
        return reverse("autoservice:technician-detail", kwargs={"pk": self.pk})

    def active_orders_count(self):
        return self.orders.filter(is_archived=False).count()


class Order(models.Model):
    client_full_name = models.CharField(max_length=60)
    client_number = models.CharField(max_length=20)
    complaint = models.TextField(blank=True)
    car_model = models.CharField(max_length=50)
    car_year = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    order_types = models.ManyToManyField(OrderType, related_name="orders")
    is_archived = models.BooleanField(default=False)
    service_advisor = models.ForeignKey(
        ServiceAdvisor,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="orders"
    )
    technicians = models.ManyToManyField(Technician, related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at} {self.car_model} {self.car_year} {self.client_full_name} {self.client_number}"

    def get_absolute_url(self):
        return reverse("autoservice:order-detail", kwargs={"pk": self.pk})