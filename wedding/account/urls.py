from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.ClientProfileDetail.as_view(), name='client_profile_detail'),
    path('login/', views.user_login, name='login'),
    path('registration/', views.user_register, name='registration'),
]