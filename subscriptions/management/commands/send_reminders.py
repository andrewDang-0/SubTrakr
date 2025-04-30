from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from datetime import date, timedelta
from subscriptions.models import Subscription

class Command(BaseCommand):
    help = 'Send email reminders for upcoming subscription renewals'

    def handle(self, *args, **kwargs):
        today = date.today()
        soon = today + timedelta(days=3)

        subs = Subscription.objects.filter(remind_method='Email', renewal_date__range=(today, soon))

        for sub in subs:
            if sub.user.email:
                send_mail(
                    subject=f"Reminder: {sub.name} renews soon!",
                    message=f"Hi {sub.user.username},\n\nYour subscription to '{sub.name}' is renewing on {sub.renewal_date}.",
                    from_email=None,
                    recipient_list=[sub.user.email],
                    fail_silently=True,
                )
                self.stdout.write(f"Sent reminder for {sub.name} to {sub.user.email}")
