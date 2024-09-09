"""The Eco Mane Config Flow."""

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant, callback

from .const import DEFAULT_IP_ADDRESS, DEFAULT_NAME, DOMAIN, SELECTOR_IP, SELECTOR_NAME

_LOGGER = logging.getLogger(__name__)


@callback
def configured_instances(hass: HomeAssistant) -> set[str]:
    """Return a set of configured instances."""

    _LOGGER.debug("configured_instances")
    return {entry.data["name"] for entry in hass.config_entries.async_entries(DOMAIN)}


class EcoManeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eco Mane."""

    VERSION = 0
    MINOR_VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        _LOGGER.debug("async_step_user")
        errors = {}
        if user_input is not None:
            # Validate user input here
            if user_input[SELECTOR_NAME] in configured_instances(self.hass):
                errors["base"] = "name_exists"
            else:
                # Additional custom validation can be added here
                return self.async_create_entry(
                    title=user_input[SELECTOR_NAME], data=user_input
                )

        data_schema = vol.Schema(
            {
                vol.Required(
                    SELECTOR_NAME,
                    default=DEFAULT_NAME,
                ): str,
                vol.Required(SELECTOR_IP, default=DEFAULT_IP_ADDRESS): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )