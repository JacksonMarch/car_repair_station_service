from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    OrderSearchForm,
    TechnicianSearchForm,
    ServiceAdvisorCreationForm,
    ServiceAdvisorUpdateForm,
    OrderForm
)
from .models import (
    Order,
    Technician,
    ServiceAdvisor,
    MasterQualification,
    OrderType
)


@login_required
def index(request):
    num_orders = Order.objects.filter(is_archived=False).count()
    active_orders_count = Order.objects.filter(
        technicians__isnull=False,
        is_archived=False,
        service_advisor__isnull=False,
    ).distinct().count()

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
    template_name = "autoservice/order/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_full_name = self.request.GET.get("client_full_name", "")
        context["search_form"] = OrderSearchForm(
            initial={"client_full_name": client_full_name})
        service_advisor_id = self.request.GET.get("service_advisor_id")
        if service_advisor_id:
            context["service_advisor"] = get_object_or_404(
                ServiceAdvisor, id=service_advisor_id
            )
        return context

    def get_queryset(self):
        queryset = Order.objects.select_related(
            "service_advisor",
        ).prefetch_related(
            "order_types",
            "technicians"
        ).filter(is_archived=False)
        client_full_name = self.request.GET.get("client_full_name")
        if client_full_name:
            queryset = queryset.filter(
                client_full_name__icontains=client_full_name
            )
        service_advisor_id = self.request.GET.get("service_advisor_id")
        if service_advisor_id:
            queryset = queryset.filter(service_advisor_id=service_advisor_id)
        return queryset


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order
    template_name = "autoservice/order/detail.html"


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = "autoservice/order/form.html"


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "autoservice/order/form.html"


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("autoservice:order-list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.is_archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
    template_name = "autoservice/order/confirm_delete.html"


class TechnicianListView(LoginRequiredMixin, generic.ListView):
    model = Technician
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        master_qualification = self.request.GET.get(
            "master_qualification", ""
        )
        context["search_form"] = TechnicianSearchForm(
            initial={"master_qualification": master_qualification}
        )
        return context

    def get_queryset(self):
        active_orders = Order.objects.filter(is_archived=False)
        queryset = Technician.objects.prefetch_related(
            Prefetch(
                "orders", queryset=active_orders, to_attr="assigned_orders"
            )
        )
        master_qualification = self.request.GET.get("master_qualification")
        if master_qualification:
            queryset = queryset.filter(
                master_qualification__name__icontains=master_qualification
            )
        return queryset
    template_name = "autoservice/technician/list.html"


class TechnicianDetailView(LoginRequiredMixin, generic.DetailView):
    model = Technician
    template_name = "autoservice/technician/detail.html"


class TechnicianOrderListView(LoginRequiredMixin, generic.ListView):
    model = Technician
    template_name = "autoservice/technician/order.html"

    def get_queryset(self):
        return Order.objects.filter(
            technicians__id=self.kwargs["pk"],
            is_archived=False
        ).prefetch_related(
            "order_types",
            "technicians"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["technician"] = Technician.objects.get(pk=self.kwargs["pk"])
        return context


class TechnicianCreateView(LoginRequiredMixin, generic.CreateView):
    model = Technician
    fields = "__all__"
    template_name = "autoservice/technician/form.html"


class TechnicianUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Technician
    fields = "__all__"
    template_name = "autoservice/technician/form.html"


class TechnicianDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Technician
    success_url = reverse_lazy("autoservice:technician-list")
    template_name = "autoservice/technician/confirm_delete.html"


class ServiceAdvisorListView(LoginRequiredMixin, generic.ListView):
    model = ServiceAdvisor
    queryset = ServiceAdvisor.objects.select_related("order")
    template_name = "autoservice/service_advisor/list.html"
    context_object_name = "service_advisor_list"

    def get_queryset(self):
        return ServiceAdvisor.objects.prefetch_related("orders")


class ServiceAdvisorDetailView(LoginRequiredMixin, generic.DetailView):
    model = ServiceAdvisor
    template_name = "autoservice/service_advisor/detail.html"
    context_object_name = "service_advisor"


class ServiceAdvisorCreateView(LoginRequiredMixin, generic.CreateView):
    model = ServiceAdvisor
    form_class = ServiceAdvisorCreationForm
    success_url = reverse_lazy("autoservice:service-advisor-list")
    template_name = "autoservice/service_advisor/form.html"


class ServiceAdvisorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = ServiceAdvisor
    form_class = ServiceAdvisorUpdateForm
    success_url = reverse_lazy("autoservice:service-advisor-list")
    template_name = "autoservice/service_advisor/form.html"


class ServiceAdvisorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ServiceAdvisor
    success_url = reverse_lazy("autoservice:service-advisor-list")
    template_name = "autoservice/service_advisor/confirm_delete.html"


class MasterQualificationListView(LoginRequiredMixin, generic.ListView):
    model = MasterQualification
    template_name = "autoservice/master_qualification/list.html"
    context_object_name = "master_qualification_list"


class MasterQualificationCreateView(LoginRequiredMixin, generic.CreateView):
    model = MasterQualification
    fields = "__all__"
    success_url = reverse_lazy("autoservice:master-qualification-list")
    template_name = "autoservice/master_qualification/form.html"


class MasterQualificationUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = MasterQualification
    fields = "__all__"
    success_url = reverse_lazy("autoservice:master-qualification-list")
    template_name = "autoservice/master_qualification/form.html"


class MasterQualificationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = MasterQualification
    success_url = reverse_lazy("autoservice:master-qualification-list")
    template_name = "autoservice/master_qualification/confirm_delete.html"


class OrderTypeListView(LoginRequiredMixin, generic.ListView):
    model = OrderType
    paginate_by = 5
    template_name = "autoservice/order_type/list.html"
    context_object_name = "order_type_list"


class OrderTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = OrderType
    fields = "__all__"
    success_url = reverse_lazy("autoservice:order-type-list")
    template_name = "autoservice/order_type/form.html"


class OrderTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = OrderType
    fields = "__all__"
    success_url = reverse_lazy("autoservice:order-type-list")
    template_name = "autoservice/order_type/form.html"


class OrderTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = OrderType
    success_url = reverse_lazy("autoservice:order-type-list")
    template_name = "autoservice/order_type/confirm_delete.html"


@login_required
def profile_redirect_view(request):
    return redirect('autoservice:service-advisor-detail', pk=request.user.pk)


class OrderArchiveListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "autoservice/order/list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Order.objects.select_related(
            "service_advisor",
        ).prefetch_related(
            "order_types",
            "technicians"
        ).filter(is_archived=True)
        client_full_name = self.request.GET.get("client_full_name")
        if client_full_name:
            queryset = queryset.filter(
                client_full_name__icontains=client_full_name
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_archive_page"] = True
        client_full_name = self.request.GET.get("client_full_name", "")
        context["search_form"] = OrderSearchForm(
            initial={"client_full_name": client_full_name}
        )
        return context


class OrderRestoreView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.is_archived = False
        order.save()
        return redirect("autoservice:order-archive-list")


@login_required
def toggle_assign_to_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    if order.service_advisor == request.user:
        order.service_advisor = None
        order.save()
    elif order.service_advisor is None:
        order.service_advisor = request.user
        order.save()
    return redirect(request.META.get("HTTP_REFERER", "autoservice:order-list"))
