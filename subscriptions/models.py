from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

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
    remind_method = models.CharField(
        max_length=10,
        choices=[('Email', 'Email'), ('In-App', 'In-App')],
        default='In-App'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
class Reminder(models.Model):
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    remind_date = models.DateField()
    method = models.CharField(max_length=50, choices=[
        ('Email', 'Email'),
        ('In-App', 'In-App'),
    ])

    def __str__(self):
        return f"Reminder for {self.subscription.name} on {self.remind_date}"

@receiver(post_save, sender=Subscription)
def create_reminder_for_subscription(sender, instance, created, **kwargs):
    if created:
        Reminder.objects.create(
            subscription=instance,
            remind_date=instance.renewal_date,
            method=instance.remind_method
        )