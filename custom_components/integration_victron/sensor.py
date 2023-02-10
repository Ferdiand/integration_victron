"""Sensor platform for integration_victron."""
from .const import DOMAIN

from .smart_solar_MPPT import add_smart_solar_mppt_sensors

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup entities platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = []

    add_smart_solar_mppt_sensors(sensors, coordinator, entry)

    async_add_devices(sensors)
