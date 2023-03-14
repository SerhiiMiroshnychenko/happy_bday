"""ПЛАНУВАЛЬНИК"""

# Планувальник
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Імпорт з пакета налаштувань
from happy_bday.settings import TIME_ZONE


# Планувальник для загальних функцій в боті
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)

# Планувальних для нагадувань
reminders_scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
