from django.urls import path

from . import views

app_name = "autoservice"

urlpatterns = [
    path("", views.index, name="index"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/create/", views.OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
    path("technician/", views.TechnicianListView.as_view(), name="technician-list"),
    path("technician/<int:pk>/", views.TechnicianDetailView.as_view(), name="technician-detail"),
    path("technician/<int:pk>/order", views.TechnicianOrderListView.as_view(), name="technician-order"),
    path("technician/create/", views.TechnicianCreateView.as_view(), name="technician-create"),
    path("technician/<int:pk>/update/", views.TechnicianUpdateView.as_view(), name="technician-update"),
    path("technician/<int:pk>/delete/", views.TechnicianDeleteView.as_view(), name="technician-delete"),
    path("service-advisor/", views.ServiceAdvisorListView.as_view(), name="service-advisor-list"),
    path("service-advisor/<int:pk>/", views.ServiceAdvisorDetailView.as_view(), name="service-advisor-detail"),
    path("service-advisor/create/", views.ServiceAdvisorCreateView.as_view(), name="service-advisor-create"),
    path("service-advisor/<int:pk>/update/", views.ServiceAdvisorUpdateView.as_view(), name="service-advisor-update"),
    path("service-advisor/<int:pk>/delete/", views.ServiceAdvisorDeleteView.as_view(), name="service-advisor-delete"),
    path("master-qualification/", views.MasterQualificationListView.as_view(), name="master-qualification-list"),
    path("master-qualification/create/", views.MasterQualificationCreateView.as_view(), name="master-qualification-create"),
    path("master-qualification/<int:pk>/update/", views.MasterQualificationUpdateView.as_view(), name="master-qualification-update"),
    path("master-qualification/<int:pk>/delete/", views.MasterQualificationDeleteView.as_view(), name="master-qualification-delete"),
    path("order-type/", views.OrderTypeListView.as_view(), name="order-type-list"),
    path("order-type/create/", views.OrderTypeCreateView.as_view(), name="order-type-create"),
    path("order-type/<int:pk>/update/", views.OrderTypeUpdateView.as_view(), name="order-type-update"),
    path("order-type/<int:pk>/delete/", views.OrderTypeDeleteView.as_view(), name="order-type-delete"),
    path("accounts/profile/", views.profile_redirect_view, name="profile-redirect"),
    path("archive/", views.OrderArchiveListView.as_view(), name="order-archive-list"),
path("orders/<int:pk>/restore/", views.OrderRestoreView.as_view(), name="order-restore"),
]