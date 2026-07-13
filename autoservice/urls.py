from django.urls import path

from .views import (
    index,
    OrderListView,
    OrderTypeListView,
    TechnicianListView,
    ServiceAdvisorListView,
    MasterQualificationListView,

)

app_name = "autoservice"

urlpatterns = [
    path("", index, name="index"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("technician/", TechnicianListView.as_view(), name="technician-list"),
    path("service-advisor/", ServiceAdvisorListView.as_view(), name="service-advisor-list"),
    path("master-qualification/", MasterQualificationListView.as_view(), name="master-qualification-list"),
    path("order-type/", OrderTypeListView.as_view(), name="order-type-list"),

]