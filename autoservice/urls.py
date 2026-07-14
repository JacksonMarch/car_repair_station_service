from django.urls import path

from .views import (
    index,
    OrderListView,
    OrderTypeListView,
    OrderTypeCreateView,
    OrderTypeUpdateView,
    OrderTypeDeleteView,
    TechnicianListView,
    TechnicianDetailView,
    TechnicianCreateView,
    TechnicianUpdateView,
    TechnicianDeleteView,
    ServiceAdvisorListView,
    ServiceAdvisorDetailView,
    ServiceAdvisorCreateView,
    ServiceAdvisorUpdateView,
    ServiceAdvisorDeleteView,
    MasterQualificationListView,
    MasterQualificationCreateView,
    MasterQualificationUpdateView,
    MasterQualificationDeleteView,

)

app_name = "autoservice"

urlpatterns = [
    path("", index, name="index"),
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("technician/", TechnicianListView.as_view(), name="technician-list"),
    path("technician/<int:pk>/", TechnicianDetailView.as_view(), name="technician-detail"),
    path("technician/create/", TechnicianCreateView.as_view(), name="technician-create"),
    path("technician/<int:pk>/update/", TechnicianUpdateView.as_view(), name="technician-update"),
    path("technician/<int:pk>/delete/", TechnicianDeleteView.as_view(), name="technician-delete"),
    path("service-advisor/", ServiceAdvisorListView.as_view(), name="service-advisor-list"),
    path("service-advisor/<int:pk>/", ServiceAdvisorDetailView.as_view(), name="service-advisor-detail"),
    path("service-advisor/create/", ServiceAdvisorCreateView.as_view(), name="service-advisor-create"),
    path("service-advisor/<int:pk>/update/", ServiceAdvisorUpdateView.as_view(), name="service-advisor-update"),
    path("service-advisor/<int:pk>/delete/", ServiceAdvisorDeleteView.as_view(), name="service-advisor-delete"),
    path("master-qualification/", MasterQualificationListView.as_view(), name="master-qualification-list"),
    path("master-qualification/create/", MasterQualificationCreateView.as_view(), name="master-qualification-create"),
    path("master-qualification/<int:pk>/update/", MasterQualificationUpdateView.as_view(), name="master-qualification-update"),
    path("master-qualification/<int:pk>/delete/", MasterQualificationDeleteView.as_view(), name="master-qualification-delete"),
    path("order-type/", OrderTypeListView.as_view(), name="order-type-list"),
    path("order-type/create/", OrderTypeCreateView.as_view(), name="order-type-create"),
    path("order-type/<int:pk>/update/", OrderTypeUpdateView.as_view(), name="order-type-update"),
    path("order-type/<int:pk>/delete/", OrderTypeDeleteView.as_view(), name="order-type-delete"),

]