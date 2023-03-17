"""ШЛЯХИ ДО СТОРІНОК САЙТУ"""

from django.urls import path
from happy_site.views import sing_out, edit_bd, edit_reminder, delete_bd, del_reminder, \
    RegisterUser, LoginUser, AddBDay, BDayList, ShowBDay, AddReminder, NextBDay

urlpatterns = [
    path('', NextBDay.as_view(), name='home'),  # http://127.0.0.1:8080/
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', sing_out, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('bdays/', BDayList.as_view(), name='b_days'),  # http://127.0.0.1:8080/bdays/
    path('bday/<int:bday_pk>/', ShowBDay.as_view(), name='bday'),
    path('add_bday/', AddBDay.as_view(), name='add_bday'),  # http://127.0.0.1:8080/add_bday/
    path('bdays/<int:bd_id>/edit', edit_bd, name='edit'),
    path('bdays/<int:bd_id>/delete', delete_bd, name='delete'),
    path('bdays/<int:bd_id>/add_reminder', AddReminder.as_view(), name='add_reminder'),
    path('edit_reminder/<int:reminder_id>', edit_reminder, name='edit_reminder'),
    path('edit_reminder/<int:reminder_id>/delete', del_reminder, name='del_reminder'),
]
