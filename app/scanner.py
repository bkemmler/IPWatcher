# scanner.py
# This file contains the network scanning logic for the IP Watcher application.

import nmap
from . import crud, schemas
from .database import SessionLocal
from .mqtt_publisher import publish_new_device
from datetime import datetime

def ping_sweep(ip_ranges: list[str]):
    """
    Performs a ping sweep of the specified IP ranges to discover new devices.
    """
    nm = nmap.PortScanner()
    for ip_range in ip_ranges:
        # Perform a ping scan (-sn) of the IP range.
        nm.scan(hosts=ip_range, arguments='-sn')
        for host in nm.all_hosts():
            db = SessionLocal()
            # If the device is not already in the database, create a new entry.
            if not crud.get_device_by_ip(db, host):
                device = schemas.DeviceCreate(ip_address=host)
                new_device = crud.create_device(db, device)
                # Publish a message to the MQTT broker to announce the new device.
                publish_new_device(new_device)
            db.close()

def deep_scan(ip_ranges: list[str]):
    """
    Performs a deep scan of the specified IP ranges to gather detailed information about devices.
    """
    nm = nmap.PortScanner()
    for ip_range in ip_ranges:
        # Perform a deep scan (-A) of the IP range.
        nm.scan(hosts=ip_range, arguments='-A')
        for host in nm.all_hosts():
            db = SessionLocal()
            device = crud.get_device_by_ip(db, host)
            # If the device is already in the database, update its information.
            if device:
                device.mac_address = nm[host]['addresses'].get('mac')
                device.vendor = nm[host]['vendor'].get(device.mac_address) if device.mac_address else None
                device.os = nm[host]['osmatch'][0]['name'] if nm[host]['osmatch'] else None
                device.open_ports = ",".join(nm[host]['tcp'].keys()) if 'tcp' in nm[host] else None
                device.last_seen = datetime.utcnow()
                db.commit()
            db.close()
