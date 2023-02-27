from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', index, name='home'),  # http://127.0.0.1:8080/
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('bdays/', BDayList.as_view(), name='b_days'),  # http://127.0.0.1:8080/bdays/
    path('bdays/<int:bd_id>/edit', edit_bd, name='edit'),
    path('add_bday/', AddBDay.as_view(), name='add_bday'),  # http://127.0.0.1:8080/add_bday/
]

