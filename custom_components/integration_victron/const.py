"""Constants for integration_blueprint."""
# Base component constants
NAME = "Integration Victron"
DOMAIN = "integration_victron"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
ID = "BLA BAL"
ATTRIBUTION = "https://github.com/Ferdiand/integration_victron"
ISSUE_URL = "https://github.com/Ferdiand/integration_victron/issues"

# Icons
ICON = "mdi:format-quote-close"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
