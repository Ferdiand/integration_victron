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

from homeassistant.exceptions import InvalidStateError


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
            OffReasonModeSensor(coordinator, entry, "Off Reason", "OR"),
            ErrorCodeSensor(coordinator, entry, "Error code", "ERR"),
            TrackerOperationModeSensor(coordinator, entry, "Tracker op", "MPPT"),
        ]
    )


class VictronSensor(IntegrationVictronEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    def __init__(self, coordinator, config_entry, name, key):
        super().__init__(coordinator, config_entry, key)
        self.coordinator._data[key] = "0.0"
        self._attr_name = name

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        return self.coordinator._data[self._key]

    @property
    def avaliable(self) -> bool:
        """Return if meassure is avalaiable"""
        if (
            self._key in self.coordinator._data[self._key]
            or self.coordinator._data[self._key] is ""
        ):
            return False
        else:
            return super().available()


class PowerSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def device_class(self) -> str | None:
        return DEVICE_CLASS_POWER

    @property
    def native_unit_of_measurement(self) -> str | None:
        return "W"

    @property
    def available(self) -> bool:
        if super().available():
            try:
                _value = float(self.coordinator._data[self._key])
                return True
            except Exception as exception:
                raise InvalidStateError() from exception
        else:
            return False


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

    @property
    def available(self) -> bool:
        if super().available():
            try:
                _value = float(self.coordinator._data[self._key])
                return True
            except Exception as exception:
                raise InvalidStateError() from exception
        else:
            return False


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

    @property
    def available(self) -> bool:
        if super().available():
            try:
                _value = float(self.coordinator._data[self._key])
                return True
            except Exception as exception:
                raise InvalidStateError() from exception
        else:
            return False


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

    @property
    def available(self) -> bool:
        if super().available():
            try:
                _value = float(self.coordinator._data[self._key])
                return True
            except Exception as exception:
                raise InvalidStateError() from exception
        else:
            return False


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
        key = super().native_value
        if key in _states:
            return _states[super().native_value]
        else:
            return key


class ErrorCodeSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def native_value(self):
        _states = {
            "0": "No error",
            "2": "Battery voltage too high",
            "17": "Charger temperature too high",
            "18": "Charger over current",
            "19": "Charger current reversed",
            "20": "Bulk time limit exceeded",
            "21": "Current sensor issue (sensor bias/sensor broken)",
            "26": "Terminals overheated",
            "28": "Converter issue (dual converter models only)",
            "33": "Input voltage too high (solar panel)",
            "34": "Input current too high (solar panel)",
            "38": "Input shutdown (due to excessive battery voltage)",
            "39": "Input shutdown (due to current flow during off mode)",
            "65": "Lost communication with one of devices",
            "66": "Synchronised charging device configuration issue",
            "67": "BMS connection lost",
            "68": "Network misconfigured",
            "116": "Factory calibration data lost",
            "117": "Invalid/incompatible firmware",
            "119": "User settings invalid",
        }
        key = super().native_value
        if key in _states:
            return _states[super().native_value]
        else:
            return key


class TrackerOperationModeSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def native_value(self):
        _states = {
            "0": "Off",
            "1": "Voltage or current limited",
            "2": "MPP Tracker active",
        }
        key = super().native_value
        if key in _states:
            return _states[super().native_value]
        else:
            return key


class OffReasonModeSensor(VictronSensor):
    """integration_blueprint Sensor class."""

    @property
    def native_value(self):
        _states = {
            "0x00000000": "No reason",
            "0x00000001": "No input power",
            "0x00000002": "Switched off (power switch)",
            "0x00000004": "Switched off (device mode register) ",
            "0x00000008": "Remote input",
            "0x00000010": "Protection active ",
            "0x00000020": "Paygo",
            "0x00000040": "BMS",
            "0x00000080": "Engine shutdown",
            "0x00000100": "Analysing input voltage",
        }
        key = super().native_value
        if key in _states:
            return _states[super().native_value]
        else:
            return key
