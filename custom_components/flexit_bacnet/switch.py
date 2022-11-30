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

COMFORT_BUTTON = SwitchEntityDescription(
    key="comfort_button",
    name="Comfort button",
    entity_category=EntityCategory.CONFIG,
)

SCHEDULER_OVERRIDE = SwitchEntityDescription(
    key="scheduler_override",
    name="Scheduler override",
    entity_category=EntityCategory.CONFIG,
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit switch."""
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        FlexitComfortSwitch(coordinator, COMFORT_BUTTON),
        FlexitCalendarOverrideSwitch(coordinator, SCHEDULER_OVERRIDE),
    ])

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
    def available(self) -> bool:
        """Entity is available"""
        return self.coordinator.device.available

    @property
    def is_on(self) -> bool:
        """Return the state."""
        return self.coordinator.device.__getattribute__(self.entity_description.key)

class FlexitComfortSwitch(FlexitSwitch):
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.coordinator.device.activate_comfort_button()
        self.update()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.coordinator.device.deactivate_comfort_button()
        self.update()

class FlexitCalendarOverrideSwitch(FlexitSwitch):
    def turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        self.coordinator.device.activate_schedule_override()
        self.update()

    def turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        self.coordinator.device.deactivate_schedule_override()
        self.update()
