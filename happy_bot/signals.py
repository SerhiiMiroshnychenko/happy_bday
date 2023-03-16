"""ЗВ'ЯЗОК ЧЕРЕЗ SIGNALS З HAPPY SITE"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
from happy_site.models import Reminder
