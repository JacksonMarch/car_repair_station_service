from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from autoservice.models import ServiceAdvisor, Order, OrderType, Technician


class ServiceAdvisorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = ServiceAdvisor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )


class ServiceAdvisorUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceAdvisor
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class OrderSearchForm(forms.Form):
    client_full_name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by client name"}),
    )


class TechnicianSearchForm(forms.Form):
    master_qualification = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by qualification"}),
    )


class OrderForm(forms.ModelForm):
    order_type = forms.ModelMultipleChoiceField(
        queryset=OrderType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    technician = forms.ModelMultipleChoiceField(
        queryset=Technician.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Order
        exclude = ["is_archived", "created_at"]
