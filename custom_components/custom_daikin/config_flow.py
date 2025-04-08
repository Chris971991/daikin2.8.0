"""Config flow for Custom Daikin integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import CONF_KEY, CONF_UUID, DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_PASSWORD): str,
        vol.Optional(CONF_KEY): str,
        vol.Optional(CONF_UUID): str,
    }
)

async def validate_input(hass: HomeAssistant, data):
    """Validate the user input allows us to connect."""
    from .pydaikin.factory import DaikinFactory
    
    host = data[CONF_HOST]
    password = data.get(CONF_PASSWORD)
    key = data.get(CONF_KEY)
    uuid = data.get(CONF_UUID)
    
    try:
        device = await DaikinFactory(
            host,
            password=password,
            key=key,
            uuid=uuid
        )
        
        # Get device info for the title
        name = device.name if hasattr(device, "name") else host
        
        return {"title": name}
    except Exception as err:
        _LOGGER.error("Error connecting to Daikin device: %s", err)
        raise


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Custom Daikin."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    
    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                
                # Check if device already configured
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                
                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )
            except Exception:
                errors["base"] = "cannot_connect"
        
        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )