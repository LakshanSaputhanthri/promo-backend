from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.features.hnb import refresh_hnb_promotions
import logging

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(
        refresh_hnb_promotions,
        CronTrigger(hour=00, minute=0),
        id="refresh_hnb_promotions",
        replace_existing=True,
        max_instances=1,
    )
    scheduler.start()
    logging.info("Scheduler started: refresh_hnb_promotions at 12:00 PM")
