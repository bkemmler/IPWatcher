# mqtt_publisher.py
# This file contains the MQTT publishing logic for the IP Watcher application.

import paho.mqtt.client as mqtt
import json
from .config import settings
from .schemas import Device

def publish_new_device(device: Device):
    """
    Publishes a new device to the MQTT broker.
    This function is called when a new device is discovered on the network.
    It publishes a message to the MQTT broker to announce the new device.
    The message is formatted for Home Assistant's MQTT discovery protocol.
    """
    # Create a new MQTT client.
    client = mqtt.Client()

    # Set the username and password if they are configured.
    if settings.mqtt.username:
        client.username_pw_set(settings.mqtt.username, settings.mqtt.password)

    # Connect to the MQTT broker.
    client.connect(settings.mqtt.broker_url)

    # Create the payload for the attributes topic.
    payload = {
        "ip_address": device.ip_address,
        "mac_address": device.mac_address,
        "vendor": device.vendor,
        "first_seen": device.first_seen.isoformat(),
    }

    # Publish the Home Assistant discovery configuration payload.
    # This message tells Home Assistant how to create a new device tracker entity.
    client.publish(
        f"{settings.mqtt.topic}/{device.ip_address.replace('.', '_')}/config",
        json.dumps({
            "name": f"IP Watcher {device.ip_address}",
            "unique_id": f"ip_watcher_{device.ip_address}",
            "state_topic": f"{settings.mqtt.topic}/{device.ip_address.replace('.', '_')}/state",
            "json_attributes_topic": f"{settings.mqtt.topic}/{device.ip_address.replace('.', '_')}/attributes",
            "device": {
                "identifiers": [f"ip_watcher_{device.ip_address}"],
                "name": f"IP Watcher {device.ip_address}",
                "model": "IP Watcher",
                "manufacturer": "Gemini",
            },
        }),
        retain=True,
    )

    # Publish the state payload.
    # This message tells Home Assistant that the device is online.
    client.publish(
        f"{settings.mqtt.topic}/{device.ip_address.replace('.', '_')}/state",
        "online",
        retain=True,
    )

    # Publish the attributes payload.
    # This message provides additional information about the device.
    client.publish(
        f"{settings.mqtt.topic}/{device.ip_address.replace('.', '_')}/attributes",
        json.dumps(payload),
        retain=True,
    )

    # Disconnect from the MQTT broker.
    client.disconnect()
