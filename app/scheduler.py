# scheduler.py
# This file contains the scheduling logic for the IP Watcher application.

from apscheduler.schedulers.background import BackgroundScheduler
from config import settings
from scanner import scan_network

# Create a new background scheduler.
scheduler = BackgroundScheduler()

def schedule_jobs():
    """
    Schedule the network scan job.
    """
    # Schedule the network scan to run at a regular interval.
    scheduler.add_job(
        scan_network,
        "interval",
        seconds=settings.ping_sweep_interval,
        args=[settings.ip_ranges],
        id="network_scan",
        replace_existing=True,
    )

# Schedule the jobs when the application starts.
schedule_jobs()