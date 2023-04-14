from django.urls import path
from .views import class_views

urlpatterns = [
    path('service-order', class_views.ServiceOrderAPIView.as_view()),
    path('authenticate', class_views.LoginAPIView.as_view())
]