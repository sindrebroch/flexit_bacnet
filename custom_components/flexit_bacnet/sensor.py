
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import FlexitDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FlexitSensor(coordinator, SensorEntityDescription(
        name="Test",
        key="flexit_local_test"
    ))])


class FlexitSensor(CoordinatorEntity, SensorEntity):

    coordinator: FlexitDataUpdateCoordinator

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: SensorEntityDescription,
    ) -> None:

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        LOGGER.warn("SENSOR")
        isvalid = self.coordinator.device.is_valid()
        LOGGER.warn(isvalid)
        LOGGER.warn(self.coordinator.device.device_name)
        LOGGER.warn(self.coordinator.device.serial_number)

    @property
    def native_value(self) -> StateType:
        return "Test"

