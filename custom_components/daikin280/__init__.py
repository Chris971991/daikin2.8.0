"""The Custom Daikin integration."""
import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Custom Daikin component."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Daikin from a config entry."""
    from .pydaikin.factory import DaikinFactory
    
    try:
        host = entry.data["host"]
        password = entry.data.get("password")
        key = entry.data.get("key")
        uuid = entry.data.get("uuid")
        
        daikin_api = await DaikinFactory(
            host, 
            password=password, 
            key=key, 
            uuid=uuid
        )
        
        hass.data[DOMAIN][entry.entry_id] = daikin_api
        
    except Exception as err:
        _LOGGER.error("Error connecting to Daikin device: %s", err)
        raise ConfigEntryNotReady from err
    
    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok