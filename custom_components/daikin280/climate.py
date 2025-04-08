"""Support for Daikin AC units."""
import logging
from typing import Any, Dict, List, Optional

from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ATTR_FAN_MODE,
    ATTR_HVAC_MODE,
    ATTR_PRESET_MODE,
    ATTR_SWING_MODE,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Map Daikin HVAC modes to Home Assistant modes
HVAC_MODE_MAPPING = {
    "off": HVACMode.OFF,
    "auto": HVACMode.AUTO,
    "cool": HVACMode.COOL,
    "heat": HVACMode.HEAT,
    "fan_only": HVACMode.FAN_ONLY,
    "dry": HVACMode.DRY,
}

# Map Home Assistant modes to Daikin HVAC modes
HVAC_MODE_REVERSE_MAPPING = {v: k for k, v in HVAC_MODE_MAPPING.items()}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Daikin climate based on config_entry."""
    daikin_api = hass.data[DOMAIN][entry.entry_id]
    
    async_add_entities([DaikinClimate(daikin_api)], update_before_add=True)


class DaikinClimate(ClimateEntity):
    """Representation of a Daikin HVAC."""

    _attr_temperature_unit = TEMP_CELSIUS
    _enable_turn_on_off_backwards_compatibility = False

    def __init__(self, api):
        """Initialize the climate device."""
        self._api = api
        self._attr_unique_id = f"{api.mac}-climate"
        self._attr_name = f"{api.name} Climate"
        
        # Set supported features based on the device capabilities
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
        )
        
        if hasattr(api, "swing_modes") and api.swing_modes:
            self._attr_supported_features |= ClimateEntityFeature.SWING_MODE
        
        if hasattr(api, "preset_modes") and api.preset_modes:
            self._attr_supported_features |= ClimateEntityFeature.PRESET_MODE
        
        # Set available modes
        self._attr_hvac_modes = [HVACMode.OFF]
        for mode in api.available_modes:
            ha_mode = HVAC_MODE_MAPPING.get(mode)
            if ha_mode and ha_mode not in self._attr_hvac_modes:
                self._attr_hvac_modes.append(ha_mode)
        
        # Set fan modes
        if hasattr(api, "fan_modes"):
            self._attr_fan_modes = api.fan_modes
        
        # Set swing modes
        if hasattr(api, "swing_modes"):
            self._attr_swing_modes = api.swing_modes
        
        # Set preset modes
        if hasattr(api, "preset_modes"):
            self._attr_preset_modes = api.preset_modes
        
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
        
        # Update current temperature
        if hasattr(self._api, "inside_temperature"):
            self._attr_current_temperature = self._api.inside_temperature
        
        # Update target temperature
        if hasattr(self._api, "target_temperature"):
            self._attr_target_temperature = self._api.target_temperature
        
        # Update HVAC mode
        if self._api.power and hasattr(self._api, "mode"):
            self._attr_hvac_mode = HVAC_MODE_MAPPING.get(
                self._api.mode, HVACMode.AUTO
            )
        else:
            self._attr_hvac_mode = HVACMode.OFF
        
        # Update fan mode
        if hasattr(self._api, "fan_rate"):
            self._attr_fan_mode = self._api.fan_rate
        
        # Update swing mode
        if hasattr(self._api, "swing_mode"):
            self._attr_swing_mode = self._api.swing_mode
        
        # Update preset mode
        if hasattr(self._api, "preset_mode"):
            self._attr_preset_mode = self._api.preset_mode
        
        # Update extra state attributes
        self._attr_extra_state_attributes = {}
        
        if hasattr(self._api, "inside_temperature"):
            self._attr_extra_state_attributes[ATTR_INSIDE_TEMPERATURE] = self._api.inside_temperature
        
        if hasattr(self._api, "outside_temperature"):
            self._attr_extra_state_attributes[ATTR_OUTSIDE_TEMPERATURE] = self._api.outside_temperature

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            await self._api.set_target_temperature(kwargs[ATTR_TEMPERATURE])
        
        # Handle additional temperature settings if needed
        if ATTR_HVAC_MODE in kwargs:
            await self.async_set_hvac_mode(kwargs[ATTR_HVAC_MODE])

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set HVAC mode."""
        if hvac_mode == HVACMode.OFF:
            await self._api.set_power(False)
            return
        
        # Turn on if currently off
        if self._api.power is False:
            await self._api.set_power(True)
        
        # Set the mode
        daikin_mode = HVAC_MODE_REVERSE_MAPPING.get(hvac_mode)
        if daikin_mode:
            await self._api.set_mode(daikin_mode)

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set fan mode."""
        await self._api.set_fan_rate(fan_mode)

    async def async_set_swing_mode(self, swing_mode: str) -> None:
        """Set swing mode."""
        if hasattr(self._api, "set_swing_mode"):
            await self._api.set_swing_mode(swing_mode)

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set preset mode."""
        if hasattr(self._api, "set_preset_mode"):
            await self._api.set_preset_mode(preset_mode)