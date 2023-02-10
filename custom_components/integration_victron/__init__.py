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

    coordinator = FufoPiCoordinator(
        hass=hass,
        logger=_LOGGER,
        name="Victron Solar",
        update_interval=timedelta(seconds=2),
    )
    # await coordinator.async_refresh()

    # if not coordinator.last_update_success:
    #    raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


class FufoPiCoordinator(DataUpdateCoordinator):
    """FufoPi coordinator"""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        name: str,
        update_interval: timedelta,
    ) -> None:
        super().__init__(hass, logger, name=name, update_interval=update_interval)

        self.smart_solar = smart_solar_MPPT(logger=logger)

    async def _async_update_data(self):
        """Update data via serial com"""
        self._data = await self.smart_solar._async_update_data()
        return self._data


class smart_solar_MPPT:
    """Smart solar VE Direct comm"""

    def __init__(self, logger: logging.Logger) -> None:
        self._data = {
            "PID": "0xA060",
            "FW": "156",
            "SER#": "HQ2129WD7QV",
            "CS": f"{random.choice(list(CS_VALUE_LIST.keys()))}",
            "MPPT": f"{random.choice(list(MPPT_VALUE_LIST.keys()))}",
            "OR": f"{random.choice(list(OR_VALUE_LIST.keys()))}",
            "HSDS": f"{random.randrange(0,365)}",
            "Checksum": "ABCDE",
            "IL": "0",
            "ERR": f"{random.choice(list(ERR_VALUE_LIST.keys()))}",
            "LOAD": "ON",
            "V": "0",
            "VPV": "0",
            "PPV": "0",
            "I": "0",
            "H19": "0",
            "H20": "0",
            "H21": "0",
            "H22": "0",
            "H23": "0",
        }

        self.logger = logger

        try:
            self._serial = serial.Serial("/dev/ttyUSB0", baudrate=19200, timeout=1)
            self.simulation = False
        except:
            self.simulation = True

    @property
    def product_id(self):
        """return product ID"""
        _raw = self._data["PID"]
        if _raw in list(PID_VALUE_LIST.keys()):
            return PID_VALUE_LIST[_raw]

        return None

    @property
    def firmware(self):
        """return firmware version"""
        return self._data["FW"]

    @property
    def serial_number(self):
        """return serial number"""
        return self._data["SER#"]

    @property
    def state_of_operation(self):
        """return state of operation"""
        _raw = self._data["CS"]
        if _raw in list(CS_VALUE_LIST.keys()):
            return CS_VALUE_LIST[_raw]

        return None

    @property
    def tracker_operation_mode(self):
        """return tracker operation mode"""
        _raw = self._data["MPPT"]
        if _raw in list(MPPT_VALUE_LIST.keys()):
            return MPPT_VALUE_LIST[_raw]

        return None

    @property
    def off_reason(self):
        """return off reason"""
        _raw = self._data["OR"]
        if _raw in list(OR_VALUE_LIST.keys()):
            return OR_VALUE_LIST[_raw]

        return None

    @property
    def day_seq_number(self):
        """return day sequence number"""
        return self._data["HSDS"]

    @property
    def checksum(self):
        """return checksum"""
        return self._data["Checksum"]

    @property
    def load_current(self):
        """return load current in mA"""
        return self._data["IL"]

    @property
    def error_reason(self):
        """return the error reason"""
        _raw = self._data["ERR"]
        if _raw in list(ERR_VALUE_LIST.keys()):
            return ERR_VALUE_LIST[_raw]

        return None

    @property
    def load_state(self):
        """return the load state"""
        return self._data["LOAD"]

    @property
    def battery_voltage(self):
        """return the battery voltage in mV"""
        return self._data["V"]

    @property
    def panel_voltage(self):
        """return the panel voltage in mV"""
        return self._data["VPV"]

    @property
    def panel_power(self):
        """return the panel power in W"""
        return self._data["PPV"]

    @property
    def battery_current(self):
        """return the battery current in mA"""
        return self._data["I"]

    @property
    def yield_total(self):
        """return the yield total in 0.01kWh"""
        return self._data["H19"]

    @property
    def yield_today(self):
        """return the yield today in 0.01kWh"""
        return self._data["H20"]

    @property
    def max_power_today(self):
        """return the max power today in W"""
        return self._data["H21"]

    @property
    def yield_yesterday(self):
        """return the yield yesterday in 0.01kWh"""
        return self._data["H22"]

    @property
    def max_power_yesterday(self):
        """return the max power yesterday in W"""
        return self._data["H23"]

    async def _async_update_data(self):
        """Update data via serial com"""
        if self.simulation is True:
            return self._data

        _buffer = self._serial.read_all().decode("ascii", "ignore").split("\r\n")
        # remove last item, may be corrupt
        _buffer.pop(-1)

        if _buffer == "":
            for _line in _buffer:
                _field = _line.split("\t")
                if len(_field) > 1:
                    _key = _field[0]
                    _value = _field[1]
                    if _key in list(self._data.keys()):
                        self._data[_key] = _value
                    else:
                        self.logger.warning(f"Key not defined {_field}")
                else:
                    self.logger.warning(f"Field structure not valid: {_field}")
        else:
            self.logger.warning(f"buffer is empty: {_buffer}")

        return self._data
      #  except Exception as exception:
      #      raise UpdateFailed() from exception


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
