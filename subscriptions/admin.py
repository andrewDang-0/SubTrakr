from django.contrib import admin
from .models import Subscription, Reminder

# Register your models here.
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'billing_cycle', 'renewal_date', 'category')
    list_filter = ('billing_cycle', 'category')
    search_fields = ('name', 'user__username')

@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'remind_date', 'method')
    list_filter = ('method',)