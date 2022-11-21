"""Switch platform for Flexit."""

from __future__ import annotations
import time

from typing import Any, Tuple

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator

SWITCHES: Tuple[SwitchEntityDescription, ...] = (
    SwitchEntityDescription(
        key="comfort_button",
        name="Comfort button",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit switch."""
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        FlexitSwitch(coordinator, description)
        for description in SWITCHES
    )

class FlexitSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a Flexit switch."""

    sensor_data: Any
    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SwitchEntityDescription,
    ) -> None:
        """Initialize a Flexit switch."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    def update(self) -> None:
        """Refresh unit state."""
        self.coordinator.device.refresh()

    @property
    def is_on(self) -> bool:
        """Return the state."""
        return self.coordinator.device.__getattribute__(self.entity_description.key)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        await self.coordinator.device.activate_comfort_button()
        self.update()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        await self.coordinator.device.deactivate_comfort_button()
        self.update()
