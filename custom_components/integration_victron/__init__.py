"""
Custom integration to integrate integration_blueprint with Home Assistant.

For more details about this integration, please refer to
https://github.com/custom-components/integration_blueprint
"""
import asyncio
from datetime import timedelta
import time
import logging
import random
import serial

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)

SCAN_INTERVAL = timedelta(seconds=1)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    coordinator = VictronDataUpdateCoordinator(hass)
    # await coordinator.async_refresh()

    # if not coordinator.last_update_success:
    #    raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(
                hass.config_entries.async_forward_entry_setup(entry, platform)
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class VictronDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        self.platforms = []
        self.data = {
            "PID": {"value": "", "timestamp": time.localtime()},
            "FW": {"value": "", "timestamp": time.localtime()},
            "SER#": {"value": "", "timestamp": time.localtime()},
            "V": {"value": "", "timestamp": time.localtime()},
            "I": {"value": "", "timestamp": time.localtime()},
            "VPV": {"value": "", "timestamp": time.localtime()},
            "PPV": {"value": "", "timestamp": time.localtime()},
            "CS": {"value": "", "timestamp": time.localtime()},
            "MPPT": {"value": "", "timestamp": time.localtime()},
            "OR": {"value": "", "timestamp": time.localtime()},
            "ERR": {"value": "", "timestamp": time.localtime()},
            "LOAD": {"value": "", "timestamp": time.localtime()},
            "H19": {"value": "", "timestamp": time.localtime()},
            "H20": {"value": "", "timestamp": time.localtime()},
            "H21": {"value": "", "timestamp": time.localtime()},
            "H22": {"value": "", "timestamp": time.localtime()},
            "H23": {"value": "", "timestamp": time.localtime()},
            "HSDS": {"value": "", "timestamp": time.localtime()},
            "Checksum": {"value": "", "timestamp": time.localtime()},
        }
        self._ser = serial.Serial("/dev/ttyUSB0", baudrate=19200, timeout=1)
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        _data = self.data
        try:
            _read = self._ser.read_all().decode("ascii", "ignore").split("\r\n")
            self.logger.warning(f"readed from serial {_read}")
            for field in _read:
                value = field.split("\t")
                if value[0] in self.data.keys():
                    try:
                        _data[value[0]] = {
                            "value": value[-1],
                            "timestamp": time.localtime(),
                        }
                    except:
                        self.logger.warning(f"There is no value field: {value}")
                else:
                    self.logger.warning(f"key value not defined: {value}")

            return _data
        except Exception as exception:
            raise UpdateFailed() from exception


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
