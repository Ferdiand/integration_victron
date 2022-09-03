"""Sensor platform for integration_blueprint."""
from homeassistant.components.sensor import (
    SensorEntity,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
)

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import IntegrationVictronEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            PowerSensor(coordinator, entry, "Panel power", "PPV"),
            VoltageSensor(coordinator, entry, "Panel voltage", "VPV"),
            VoltageSensor(coordinator, entry, "Battery voltage", "V"),
            CurrentSensor(coordinator, entry, "Battery current", "I"),
            CurrentSensor(coordinator, entry, "Load current", "IL"),
            PowerSensor(coordinator, entry, "Max power today", "H21"),
            PowerSensor(coordinator, entry, "Max power yesterday", "H23"),
            VictronSensor(coordinator, entry, "Firmware version", "FW"),
            VictronSensor(coordinator, entry, "Product ID", "PID"),
            VictronSensor(coordinator, entry, "Serial number", "SER#"),
            ChargerStateSensor(coordinator, entry, "Charger state", "CS"),
            EnergySensor(coordinator, entry, "Yield total", "H19"),
            EnergySensor(coordinator, entry, "Yield today", "H20"),
            EnergySensor(coordinator, entry, "Yield yesterday", "H22"),
        ]
    )


class VictronSensor(IntegrationVictronEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(self, coordinator, config_entry, name, key):
        super().__init__(coordinator, config_entry, key)
        self.coordinator._data[key] = 0.0
        self._attr_name = name

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator._data[self._key]


class PowerSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_POWER

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "W"


class EnergySensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_ENERGY

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "kWh"

    @property
    def native_value(self):
        return float(super().native_value) / 100


class VoltageSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_VOLTAGE

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "V"

    @property
    def native_value(self):
        return float(super().native_value) / 1000


class CurrentSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_CURRENT

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "A"

    @property
    def native_value(self):
        return float(super().native_value) / 1000


class ChargerStateSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def native_value(self):
        _states = {
            "0": "Off",
            "2": "Fault",
            "3": "Bulk",
            "4": "Absorption",
            "5": "Float",
            "6": "Storage",
            "7": "Equalize (manual)",
            "9": "Inverting",
            "11": "Power supply",
            "245": "Starting-up",
            "246": "Repeated absorption",
            "247": "Auto equalize / Recondition",
            "248": "BatterySafe",
            "252": "External Control",
        }
        return _states[super().native_value]
