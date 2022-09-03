"""Sensor platform for integration_blueprint."""
from homeassistant.components.sensor import SensorEntity

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .entity import IntegrationVictronEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([PanelPowerSensor(coordinator, entry, "PPV")])


class PowerSensor(IntegrationVictronEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return super().device_class.POWER

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "W"


class PanelPowerSensor(PowerSensor):
    """integration_blueprint Sensor class."""

    def __init__(self, coordinator, config_entry, name):
        super().__init__(coordinator, config_entry)
        self.coordinator._data["PPV"] = 0.0
        self._attr_name = name

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator._data["PPV"]
