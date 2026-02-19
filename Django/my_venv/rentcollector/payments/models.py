from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, help_text="Mpesaables phone (e.g. 2547XXXXXXXX)")

    def __str__(self):
        return self.name


class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.amount} - {'paid' if self.paid else 'pending'}"
