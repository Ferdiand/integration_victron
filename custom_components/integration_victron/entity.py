from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION, ID


class IntegrationVictronEntity(CoordinatorEntity):
    """Victron Entity class"""

    def __init__(self, coordinator, config_entry, key):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._key = key

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id + "_" + self._key

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, "HQ2129WD7QV")},
            "name": "SmartSolar charge controller",
            "model": "MPPT 100/20",
            "manufacturer": "victron energy",
            "sw_version": "1.59",
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": "HQ2129WD7QV",
            "integration": DOMAIN,
        }
