from happy_bday.settings import TIME_ZONE
from happy_bot.bd_bot import bot
# ПЛАНУВАЛЬНИК
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from happy_bot.core.handlers import schedul_task
from datetime import datetime, timedelta


"""Блок планувальника"""
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
rem_scheduler = AsyncIOScheduler(timezone=TIME_ZONE)

scheduler.add_job(schedul_task.send_message_time,
                  trigger='date', run_date=datetime.now() + timedelta(seconds=10),
                  kwargs={'bot': bot})

scheduler.add_job(schedul_task.send_message_interval,
                  trigger='interval', minutes=10, kwargs={'bot': bot})

scheduler.add_job(schedul_task.send_message_date,
                  trigger='date', run_date=schedul_task.job_date,
                  kwargs={'bot': bot})

"""Кінець блока планувальника"""

