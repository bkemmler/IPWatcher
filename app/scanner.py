# scanner.py
# This file contains the network scanning logic for the IP Watcher application.

import nmap
from . import crud, schemas
from .database import SessionLocal
from .mqtt_publisher import publish_new_device
from datetime import datetime
from mac_vendor_lookup import MacVendorLookup

def scan_network(ip_ranges: list[str]):
    """
    Performs a comprehensive scan of the specified IP ranges to discover and update devices.
    """
    nm = nmap.PortScanner()
    mac_lookup = MacVendorLookup()

    online_macs = set()

    for ip_range in ip_ranges:
        # Use -sP for ping scan and -O for OS detection. -T4 for faster execution.
        nm.scan(hosts=ip_range, arguments='-sP -O -T4')

        for host in nm.all_hosts():
            if nm[host].state() == 'up':
                mac_address = nm[host]['addresses'].get('mac')
                if mac_address:
                    online_macs.add(mac_address)
                    vendor = None
                    try:
                        vendor = mac_lookup.lookup(mac_address)
                    except KeyError:
                        pass # MAC address not in the database

                    os_details = ""
                    if 'osmatch' in nm[host] and nm[host]['osmatch']:
                        os_details = nm[host]['osmatch'][0]['name']

                    open_ports = ",".join(nm[host]['tcp'].keys()) if 'tcp' in nm[host] else ""

                    db = SessionLocal()
                    db_device = crud.get_device_by_mac(db, mac_address)

                    device_data = schemas.DeviceBase(
                        ip_address=host,
                        mac_address=mac_address,
                        vendor=vendor,
                        os_details=os_details,
                        open_ports=open_ports,
                        is_online=True,
                        last_seen=datetime.utcnow()
                    )

                    if db_device:
                        crud.update_device(db, db_device, device_data)
                        if not db_device.is_online:
                            crud.create_device_history(db, db_device.id, True)
                    else:
                        new_device = crud.create_device(db, schemas.DeviceCreate(**device_data.dict()))
                        publish_new_device(new_device)
                        crud.create_device_history(db, new_device.id, True)
                    db.close()

    db = SessionLocal()
    all_devices = crud.get_devices(db)
    for device in all_devices:
        if device.mac_address not in online_macs and device.is_online:
            device.is_online = False
            db.commit()
            crud.create_device_history(db, device.id, False)
    db.close()