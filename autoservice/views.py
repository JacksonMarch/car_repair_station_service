from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order, Technician, ServiceAdvisor, MasterQualification, OrderType


@login_required
def index(request):
    num_orders = Order.objects.count()
    active_orders_count = Order.objects.filter(technician__isnull=False).count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_orders": num_orders,
        "active_orders_count": active_orders_count,
        "num_visits": num_visits + 1,
    }

    return render(request, "autoservice/index.html", context=context)


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    paginate_by = 5
    queryset = Order.objects.select_related(
        "order_type",
        "service_advisor",
        "technician",
    )

    def get_queryset(self):
        queryset = Order.objects.select_related(
            "order_type",
            "service_advisor",
            "technician"
        )
        service_advisor_id = self.request.GET.get("service_advisor_id")
        if service_advisor_id:
            queryset = queryset.filter(service_advisor_id=service_advisor_id)
        return queryset


class TechnicianListView(LoginRequiredMixin, generic.ListView):
    model = Technician


class ServiceAdvisorListView(LoginRequiredMixin, generic.ListView):
    model = ServiceAdvisor
    queryset = ServiceAdvisor.objects.select_related("order")
    template_name = "autoservice/service_advisor_list.html"
    context_object_name = "service_advisor_list"

    def get_queryset(self):
        return ServiceAdvisor.objects.prefetch_related("orders")


class MasterQualificationListView(LoginRequiredMixin, generic.ListView):
    model = MasterQualification
    template_name = "autoservice/master_qualification_list.html"
    context_object_name = "master_qualification_list"


class OrderTypeListView(LoginRequiredMixin, generic.ListView):
    model = OrderType
    paginate_by = 5
    template_name = "autoservice/order_type_list.html"
    context_object_name = "order_type_list"


class OrderTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderType
    fields = "__all__"
    success_url = reverse_lazy("autoservice:order_type_list")
    template_name = "autoservice/order_type_form.html"


class OrderTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = OrderType
    fields = "__all__"
    success_url = reverse_lazy("autoservice:order_type_list")
    template_name = "autoservice/order_type_form.html"
