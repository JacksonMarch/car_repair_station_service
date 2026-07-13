from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ServiceAdvisor, Order, Technician, OrderType, MasterQualification


@admin.register(ServiceAdvisor)
class ServiceAdvisorAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client_full_name", "car_model", "car_year", "order_type", "service_advisor", "created_at")
    search_fields = ("client_full_name", "client_number", "car_model", "complaint")
    list_filter = ("order_type", "service_advisor", "technician", "created_at")
    date_hierarchy = "created_at"


admin.site.register(Technician)
admin.site.register(OrderType)
admin.site.register(MasterQualification)
