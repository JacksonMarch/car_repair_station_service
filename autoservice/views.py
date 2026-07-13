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



class TechnicianListView(LoginRequiredMixin, generic.ListView):
    model = Technician


class ServiceAdvisorListView(LoginRequiredMixin, generic.ListView):
    model = ServiceAdvisor
    queryset = ServiceAdvisor.objects.select_related("order")


class MasterQualificationListView(LoginRequiredMixin, generic.ListView):
    model = MasterQualification


class OrderTypeListView(LoginRequiredMixin, generic.DetailView):
    model = OrderType
    paginate_by = 5
