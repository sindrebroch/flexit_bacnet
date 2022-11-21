"""Diagnostics support for Flexit."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    config_entry: ConfigEntry
) -> dict:
    """Return diagnostics for a config entry."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]

    return {
        "flexit_bacnet": str(coordinator.device._state),
    }
