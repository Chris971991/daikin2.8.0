"""Support for Daikin AC sensors."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    POWER_KILO_WATT,
    ENERGY_KILO_WATT_HOUR,
    TEMP_CELSIUS,
    FREQUENCY_HERTZ,
)
from homeassistant.helpers.entity import DeviceInfo

from .const import (
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    ATTR_HUMIDITY,
    ATTR_COMPRESSOR_FREQUENCY,
    ATTR_TOTAL_POWER,
    ATTR_COOL_ENERGY,
    ATTR_HEAT_ENERGY,
    ATTR_DAILY_COOL_ENERGY,
    ATTR_DAILY_HEAT_ENERGY,
    ATTR_CURRENT_TOTAL_POWER,
    ATTR_CURRENT_COOL_POWER,
    ATTR_CURRENT_HEAT_POWER,
    DOMAIN,
    KEY_INSIDE_TEMPERATURE,
    KEY_OUTSIDE_TEMPERATURE,
    KEY_HUMIDITY,
    KEY_COMPRESSOR_FREQUENCY,
    KEY_COOL_ENERGY,
    KEY_HEAT_ENERGY,
    KEY_DAILY_COOL_ENERGY,
    KEY_DAILY_HEAT_ENERGY,
    KEY_CURRENT_TOTAL_POWER,
    KEY_CURRENT_COOL_POWER,
    KEY_CURRENT_HEAT_POWER,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_HUMIDITY,
    SENSOR_TYPE_POWER,
    SENSOR_TYPE_ENERGY,
    SENSOR_TYPE_FREQUENCY,
)

_LOGGER = logging.getLogger(__name__)

# Sensor configuration
SENSOR_TYPES = {
    ATTR_INSIDE_TEMPERATURE: {
        "key": KEY_INSIDE_TEMPERATURE,
        "name": "Inside Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": TEMP_CELSIUS,
        "icon": "mdi:thermometer",
        "type": SENSOR_TYPE_TEMPERATURE,
    },
    ATTR_OUTSIDE_TEMPERATURE: {
        "key": KEY_OUTSIDE_TEMPERATURE,
        "name": "Outside Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": TEMP_CELSIUS,
        "icon": "mdi:thermometer",
        "type": SENSOR_TYPE_TEMPERATURE,
    },
    ATTR_HUMIDITY: {
        "key": KEY_HUMIDITY,
        "name": "Humidity",
        "device_class": SensorDeviceClass.HUMIDITY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
        "icon": "mdi:water-percent",
        "type": SENSOR_TYPE_HUMIDITY,
    },
    ATTR_COMPRESSOR_FREQUENCY: {
        "key": KEY_COMPRESSOR_FREQUENCY,
        "name": "Compressor Frequency",
        "device_class": SensorDeviceClass.FREQUENCY,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": FREQUENCY_HERTZ,
        "icon": "mdi:sine-wave",
        "type": SENSOR_TYPE_FREQUENCY,
    },
    ATTR_COOL_ENERGY: {
        "key": KEY_COOL_ENERGY,
        "name": "Cool Energy Consumption",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": ENERGY_KILO_WATT_HOUR,
        "icon": "mdi:snowflake",
        "type": SENSOR_TYPE_ENERGY,
    },
    ATTR_HEAT_ENERGY: {
        "key": KEY_HEAT_ENERGY,
        "name": "Heat Energy Consumption",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL_INCREASING,
        "unit": ENERGY_KILO_WATT_HOUR,
        "icon": "mdi:fire",
        "type": SENSOR_TYPE_ENERGY,
    },
    ATTR_DAILY_COOL_ENERGY: {
        "key": KEY_DAILY_COOL_ENERGY,
        "name": "Daily Cool Energy Consumption",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL,
        "unit": ENERGY_KILO_WATT_HOUR,
        "icon": "mdi:snowflake",
        "type": SENSOR_TYPE_ENERGY,
    },
    ATTR_DAILY_HEAT_ENERGY: {
        "key": KEY_DAILY_HEAT_ENERGY,
        "name": "Daily Heat Energy Consumption",
        "device_class": SensorDeviceClass.ENERGY,
        "state_class": SensorStateClass.TOTAL,
        "unit": ENERGY_KILO_WATT_HOUR,
        "icon": "mdi:fire",
        "type": SENSOR_TYPE_ENERGY,
    },
    ATTR_CURRENT_TOTAL_POWER: {
        "key": KEY_CURRENT_TOTAL_POWER,
        "name": "Current Power Consumption",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": POWER_KILO_WATT,
        "icon": "mdi:flash",
        "type": SENSOR_TYPE_POWER,
    },
    ATTR_CURRENT_COOL_POWER: {
        "key": KEY_CURRENT_COOL_POWER,
        "name": "Current Cool Power Consumption",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": POWER_KILO_WATT,
        "icon": "mdi:snowflake",
        "type": SENSOR_TYPE_POWER,
    },
    ATTR_CURRENT_HEAT_POWER: {
        "key": KEY_CURRENT_HEAT_POWER,
        "name": "Current Heat Power Consumption",
        "device_class": SensorDeviceClass.POWER,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": POWER_KILO_WATT,
        "icon": "mdi:fire",
        "type": SENSOR_TYPE_POWER,
    },
}


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin sensors based on config_entry."""
    daikin_api = hass.data[DOMAIN][entry.entry_id]
    
    sensors = []
    
    # Create sensors based on available data
    for sensor_type, sensor_info in SENSOR_TYPES.items():
        key = sensor_info["key"]
        
        # Check if this sensor is supported by the device
        if hasattr(daikin_api, key) or key in daikin_api.values:
            sensors.append(
                DaikinSensor(
                    daikin_api,
                    sensor_type,
                    sensor_info,
                )
            )
    
    async_add_entities(sensors, update_before_add=True)


class DaikinSensor(SensorEntity):
    """Representation of a Daikin Sensor."""

    def __init__(
        self,
        api,
        sensor_type: str,
        sensor_info: Dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        self._api = api
        self._sensor_type = sensor_type
        self._sensor_info = sensor_info
        self._key = sensor_info["key"]
        
        # Set entity attributes
        self._attr_name = f"{api.name} {sensor_info['name']}"
        self._attr_unique_id = f"{api.mac}-{sensor_type}"
        self._attr_device_class = sensor_info.get("device_class")
        self._attr_state_class = sensor_info.get("state_class")
        self._attr_native_unit_of_measurement = sensor_info.get("unit")
        self._attr_icon = sensor_info.get("icon")
        
        # Set device info
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, api.mac)},
            name=api.name,
            manufacturer="Daikin",
            model=getattr(api, "model", "Unknown"),
            sw_version=getattr(api, "firmware_version", None),
        )

    async def async_update(self) -> None:
        """Retrieve latest state."""
        await self._api.update_status()
        
        # Get the value from the API
        if hasattr(self._api, self._key):
            self._attr_native_value = getattr(self._api, self._key)
        elif self._key in self._api.values:
            value = self._api.values.get(self._key)
            
            # Convert to appropriate type based on sensor type
            if self._sensor_info["type"] == SENSOR_TYPE_TEMPERATURE:
                try:
                    self._attr_native_value = float(value)
                except (ValueError, TypeError):
                    self._attr_native_value = None
            elif self._sensor_info["type"] in (SENSOR_TYPE_POWER, SENSOR_TYPE_ENERGY, SENSOR_TYPE_FREQUENCY):
                try:
                    self._attr_native_value = float(value)
                except (ValueError, TypeError):
                    self._attr_native_value = None
            elif self._sensor_info["type"] == SENSOR_TYPE_HUMIDITY:
                try:
                    self._attr_native_value = int(value)
                except (ValueError, TypeError):
                    self._attr_native_value = None
            else:
                self._attr_native_value = value
        else:
            self._attr_native_value = None