"""ПЛАНУВАЛЬНИК"""

# Планувальник
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Імпорт з пакета налаштувань
from happy_bday.settings import TIME_ZONE


scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
reminders_scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
