from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("autoservice.urls", namespace="autoservice")),
    path("accounts/", include("django.contrib.auth.urls")),
]
