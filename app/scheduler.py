# scheduler.py
# This file contains the scheduling logic for the IP Watcher application.

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .config import settings
from .scanner import ping_sweep, deep_scan

# Create a new background scheduler.
scheduler = BackgroundScheduler()

def schedule_jobs():
    """
    Schedule the ping sweep and deep scan jobs.
    """
    # Schedule the ping sweep to run at a regular interval.
    scheduler.add_job(
        ping_sweep,
        "interval",
        seconds=settings.ping_sweep_interval,
        args=[settings.ip_ranges],
        id="ping_sweep",
        replace_existing=True,
    )
    # Schedule the deep scan to run on a cron-style schedule.
    scheduler.add_job(
        deep_scan,
        CronTrigger.from_crontab(settings.deep_scan_schedule),
        args=[settings.ip_ranges],
        id="deep_scan",
        replace_existing=True,
    )

# Schedule the jobs when the application starts.
schedule_jobs()
