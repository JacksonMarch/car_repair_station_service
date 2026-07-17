from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Order,
    OrderType,
    Technician,
    ServiceAdvisor,
    MasterQualification
)


@admin.register(ServiceAdvisor)
class ServiceAdvisorAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "is_staff"
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_full_name",
        "car_model",
        "car_year",
        "service_advisor",
        "created_at"
    )
    search_fields = (
        "client_full_name",
        "client_number",
        "car_model",
        "complaint"
    )
    list_filter = (
        "order_types",
        "service_advisor",
        "technicians",
        "created_at"
    )
    date_hierarchy = "created_at"

    def display_technicians(self, obj):
        return ", ".join([f"{tech.first_name} {tech.last_name}" for tech in obj.technicians.all()])
    display_technicians.short_description = "Technicians"

    def display_order_types(selfself, obj):
        return ", ".join([order_type.name for order_type in obj.order_types.all()])
    display_order_types.short_description = "Order Types"

admin.site.register(Technician)
admin.site.register(OrderType)
admin.site.register(MasterQualification)
