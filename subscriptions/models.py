from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subscription(models.Model):
    BILLING_CYCLE_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLE_CHOICES)
    renewal_date = models.DateField()
    category = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
class Reminder(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    remind_date = models.DateField()
    method = models.CharField(max_length=50, choices=[
        ('Email', 'Email'),
        ('In-App', 'In-App'),
    ])

    def __str__(self):
        return f"Reminder for {self.subscription.name} on {self.remind_date}"