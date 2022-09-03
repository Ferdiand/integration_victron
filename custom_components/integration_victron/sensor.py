"""Sensor platform for integration_blueprint."""
from homeassistant.components.sensor import (
    SensorEntity,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_VOLTAGE,
    DEVICE_CLASS_CURRENT,
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
            CurrentSensor(coordinator, entry, "Load current", "I"),
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
        return super().native_value / 1000


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
        return super().native_value / 1000
