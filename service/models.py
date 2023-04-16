from django.db import models

from user.models import User as UserModel


# Create your models here.
class RepairService(models.Model):
    """this modal is the type of service that owner offers"""

    service_type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )
    device_type = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )
    base_cost = models.IntegerField(null=False, blank=False)

    def __str__(self) -> str:
        return f"{self.service_type} || {self.device_type} || {self.base_cost}"


class ServiceRequest(models.Model):
    """This the service request when user submit his service request"""

    STATUS_CHOICE = (
        ("SB", "Submitted"),
        ("SH", "Shipping"),
        ("RS", "Repair"),
        ("D", "Delivered"),
        ("DT", "Deleted"),
    )

    title = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        default=" ",
    )
    description = models.TextField(blank=True, null=True)
    User = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, verbose_name="serviceuser"
    )
    date = models.DateField(auto_now_add=True)
    staff = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="staff_user",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICE,
        default="SB",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    repair_service = models.ForeignKey(
        RepairService,
        on_delete=models.CASCADE,
    )

    def soft_delete(self):
        """_"""
        self.status = "DT"
        self.save()
