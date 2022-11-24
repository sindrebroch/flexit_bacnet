from typing import Any, Dict, List

import voluptuous as vol
from voluptuous.schema_builder import Schema

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_ADDRESS, CONF_DEVICE_ID, CONF_INTERVAL, DEFAULT_INTERVAL

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="Flexit Local"): str,
        vol.Required(CONF_ADDRESS): str,
        vol.Required(CONF_DEVICE_ID): int,
    }
)

class FlexitFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a Flexit config flow."""

    VERSION = 1


    async def async_step_user(
        self,
        user_input: Dict[str, Any] or None = None,
    ) -> FlowResult:
        """Handle a flow initiated by the user."""

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
                errors={},
                last_step=True,
            )

        self.user_input = user_input
        self.title = user_input[CONF_NAME].title()

        return self.async_create_entry(
            title=self.title,
            data={**user_input, **self.user_input},
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return FlexitOptionsFlowHandler(config_entry)

class FlexitOptionsFlowHandler(OptionsFlow):
    """Handle Flexit client options."""

    def __init__(self, config_entry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, 
        user_input: Dict[str, Any] or None = None
    ) -> FlowResult:
        """Manage Flexit options."""

        if user_input is not None:
            return self.async_create_entry(title="Options", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {vol.Required(CONF_INTERVAL, default=DEFAULT_INTERVAL): int}
            ),
        )
