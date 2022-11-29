"""Support for getting statistical data from a Flexit system."""

from typing import Any, Tuple, cast

import math

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator


FILTER_BINARY_SENSORS: Tuple[BinarySensorEntityDescription, ...] = (
    BinarySensorEntityDescription(
        name="Dirty filter",
        key="air_filter_polluted",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Flexit sensor."""
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        FlexitFilterBinarySensor(coordinator, description)
        for description in FILTER_BINARY_SENSORS
    )


class FlexitBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Flexit binary sensor."""

    coordinator: FlexitDataUpdateCoordinator
    sensor_data: Any

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize a Flexit binary sensor."""

        super().__init__(coordinator)

        self.entity_description = description
        self.coordinator = coordinator
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        sensor_data = self.coordinator.device.__getattribute__(self.entity_description.key)
        return cast(bool, sensor_data)


class FlexitFilterBinarySensor(FlexitBinarySensor):
    """Binary sensor for filter."""

    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return "mdi:hvac" if self.is_on else "mdi:hvac-off"

    @property
    def available(self) -> bool:
        """Entity is available"""
        return self.coordinator.device.available

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""

        operating_time = self.coordinator.device.air_filter_operating_time
        exchange_time = self.coordinator.device.air_filter_exchange_interval
        operating_time_days = math.floor(operating_time / 24)
        exchange_time_days = math.floor(exchange_time / 24)

        return {
            "hours_since_change": operating_time,
            "filter_change_interval_hours": exchange_time,
            "hours_until_dirty": exchange_time - operating_time,
            "days_since_change": operating_time_days,
            "filter_change_interval_days": exchange_time_days,
            "days_until_dirty": exchange_time_days - operating_time_days
        }

