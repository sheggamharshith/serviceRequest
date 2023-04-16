from django import forms

from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):

    """_"""

    class Meta:
        """_"""

        model = ServiceRequest
        fields = "__all__"
