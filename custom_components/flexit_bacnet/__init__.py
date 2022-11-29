import asyncio
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.const import CONF_NAME
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    DOMAIN, 
    LOGGER, 
    PLATFORMS, 
    CONF_ADDRESS, 
    CONF_DEVICE_ID,
    CONF_INTERVAL,
    DEFAULT_INTERVAL,
)
from .coordinator import FlexitDataUpdateCoordinator
from .lib import FlexitBACnet

async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        LOGGER.info("Flexit Bacnet startup")

    if not entry.options:
        hass.config_entries.async_update_entry(
            entry,
            options={
                CONF_INTERVAL: entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL),
            },
        )

    device = FlexitBACnet(
        entry.data[CONF_ADDRESS], 
        entry.data[CONF_DEVICE_ID]
    )
    is_valid = await hass.async_add_executor_job(device.is_valid)
    if not is_valid:
        return False

    coordinator = FlexitDataUpdateCoordinator(
        hass,
        name=entry.data[CONF_NAME],
        device=device,
        update_interval=entry.options.get(CONF_INTERVAL, DEFAULT_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass, entry):
    """Unload entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        await hass.async_add_executor_job(hass.data[DOMAIN][entry.entry_id].device.disconnect)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
