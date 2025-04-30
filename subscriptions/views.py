from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Subscription, Reminder
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .forms import SubscriptionForm, CustomUserCreationForm

@login_required
def home(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    today = date.today()
    soon = today + timedelta(days=3)
    for sub in subscriptions:
        if sub.renewal_date < today:
            if sub.billing_cycle == 'Monthly':
                sub.renewal_date += relativedelta(months=1)
            elif sub.billing_cycle == 'Yearly':
                sub.renewal_date += relativedelta(years=1)
            sub.save()
        sub.is_upcoming = today <= sub.renewal_date <= soon
    return render(request, 'home.html', {'subscriptions': subscriptions})

@login_required
def add_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('home')
    else:
        form = SubscriptionForm()
    return render(request, 'add_subscription.html', {'form': form})


@login_required
def edit_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, instance=subscription)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubscriptionForm(instance=subscription)
    return render(request, 'edit_subscription.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})