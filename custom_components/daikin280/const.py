"""Constants for the Custom Daikin integration."""
from homeassistant.const import (
    CONF_HOST,
    CONF_PASSWORD,
    TEMP_CELSIUS,
)

DOMAIN = "custom_daikin"
PLATFORMS = ["climate", "sensor"]

# Config attributes
CONF_KEY = "key"
CONF_UUID = "uuid"

# Attributes
ATTR_INSIDE_TEMPERATURE = "inside_temperature"
ATTR_OUTSIDE_TEMPERATURE = "outside_temperature"
ATTR_TARGET_TEMPERATURE = "target_temperature"
ATTR_HUMIDITY = "humidity"
ATTR_TARGET_HUMIDITY = "target_humidity"
ATTR_COMPRESSOR_FREQUENCY = "compressor_frequency"
ATTR_TOTAL_POWER = "total_power"
ATTR_COOL_ENERGY = "cool_energy"
ATTR_HEAT_ENERGY = "heat_energy"
ATTR_DAILY_COOL_ENERGY = "daily_cool_energy"
ATTR_DAILY_HEAT_ENERGY = "daily_heat_energy"
ATTR_CURRENT_TOTAL_POWER = "current_total_power"
ATTR_CURRENT_COOL_POWER = "current_cool_power"
ATTR_CURRENT_HEAT_POWER = "current_heat_power"

# Sensor types
SENSOR_TYPE_TEMPERATURE = "temperature"
SENSOR_TYPE_HUMIDITY = "humidity"
SENSOR_TYPE_POWER = "power"
SENSOR_TYPE_ENERGY = "energy"
SENSOR_TYPE_FREQUENCY = "frequency"

# Sensor keys
KEY_INSIDE_TEMPERATURE = "htemp"
KEY_OUTSIDE_TEMPERATURE = "otemp"
KEY_TARGET_TEMPERATURE = "stemp"
KEY_HUMIDITY = "shum"
KEY_TARGET_HUMIDITY = "hhum"
KEY_COMPRESSOR_FREQUENCY = "cmpfreq"
KEY_COOL_ENERGY = "cool_energy"
KEY_HEAT_ENERGY = "heat_energy"
KEY_DAILY_COOL_ENERGY = "daily_cool_energy"
KEY_DAILY_HEAT_ENERGY = "daily_heat_energy"
KEY_CURRENT_TOTAL_POWER = "current_total_power"
KEY_CURRENT_COOL_POWER = "current_cool_power"
KEY_CURRENT_HEAT_POWER = "current_heat_power"