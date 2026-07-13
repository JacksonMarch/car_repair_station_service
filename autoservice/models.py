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
        verbose_name = "manager"
        verbose_name_plural = "managers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("autoservice:manager-detail", kwargs={"pk": self.pk})


class Technician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    master_qualification = models.ForeignKey(MasterQualification, on_delete=models.CASCADE)
    experience = models.TextField(blank=True)

    class Meta:
        ordering = ["master_qualification"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.master_qualification})"


class Order(models.Model):
    client_full_name = models.CharField(max_length=60)
    client_number = models.CharField(max_length=20)
    complaint = models.TextField(blank=True)
    car_model = models.CharField(max_length=50)
    car_year = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    order_type = models.ForeignKey(OrderType, on_delete=models.SET_NULL, null=True)
    service_advisor = models.ForeignKey(
        ServiceAdvisor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )
    technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at} {self.car_model} {self.car_year} {self.client_full_name} {self.client_number}"
