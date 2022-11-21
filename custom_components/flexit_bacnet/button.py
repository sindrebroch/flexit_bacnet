"""Button for Flexit."""

import time

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator

COOKER_HOOD_ON = ButtonEntityDescription(
    key="activate_cooker_hood",
    name="Activate Cooker hood",
)
COOKER_HOOD_OFF = ButtonEntityDescription(
    key="deactivate_cooker_hood",
    name="Deactivate Cooker hood",
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add Flexit entities from a config_entry."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            FlexitActivateCookerhoodButton(coordinator, COOKER_HOOD_ON),
            FlexitDeactivateCookerhoodButton(coordinator, COOKER_HOOD_OFF),
        ]
    )


class FlexitButton(CoordinatorEntity, ButtonEntity):
    """Define a Flexit entity."""

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: ButtonEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description

        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

class FlexitActivateCookerhoodButton(FlexitButton):
    async def async_press(self) -> None:
        self.coordinator.device.activate_cooker_hood()

class FlexitDeactivateCookerhoodButton(FlexitButton):
    async def async_press(self) -> None:
        self.coordinator.device.deactivate_cooker_hood()