from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_subscription, name='add_subscription'),
    path('edit/<int:pk>/', views.edit_subscription, name='edit_subscription'),
    path('signup/', views.signup, name='signup'),

]
