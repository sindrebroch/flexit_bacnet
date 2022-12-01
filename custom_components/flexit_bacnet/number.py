"""Number platform for Flexit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple, Literal

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.components.number.const import (
    DEFAULT_MAX_VALUE,
    DEFAULT_MIN_VALUE,
    MODE_AUTO,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, TIME_MINUTES
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import FlexitDataUpdateCoordinator


@dataclass
class FlexitNumberEntityDescription(NumberEntityDescription):
    """A class that describes number entities."""

    native_min_value: float | None = None
    native_max_value: float | None = None
    entity: str | None = None


SETPOINT_HOME_SUPPLY = FlexitNumberEntityDescription(
    key="fan_setpoint_supply_air_home",
    name="Fan Setpoint Home Supply",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_HOME_EXTRACT = FlexitNumberEntityDescription(
    key="fan_setpoint_extract_air_home",
    name="Fan Setpoint Home Extract",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_AWAY_SUPPLY = FlexitNumberEntityDescription(
    key="fan_setpoint_supply_air_away",
    name="Fan Setpoint Away Supply",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_AWAY_EXTRACT = FlexitNumberEntityDescription(
    key="fan_setpoint_extract_air_away",
    name="Fan Setpoint Away Extract",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_HIGH_SUPPLY = FlexitNumberEntityDescription(
    key="fan_setpoint_supply_air_high",
    name="Fan Setpoint High Supply",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_HIGH_EXTRACT = FlexitNumberEntityDescription(
    key="fan_setpoint_extract_air_high",
    name="Fan Setpoint High Extract",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_FIRE_SUPPLY = FlexitNumberEntityDescription(
    key="fan_setpoint_supply_air_fire",
    name="Fan Setpoint Fire Supply",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_FIRE_EXTRACT = FlexitNumberEntityDescription(
    key="fan_setpoint_extract_air_fire",
    name="Fan Setpoint Fire Extract",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_COOKER_SUPPLY = FlexitNumberEntityDescription(
    key="fan_setpoint_supply_air_cooker",
    name="Fan Setpoint Cooker Supply",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)
SETPOINT_COOKER_EXTRACT = FlexitNumberEntityDescription(
    key="fan_setpoint_extract_air_cooker",
    name="Fan Setpoint Cooker Extract",
    native_unit_of_measurement=PERCENTAGE,
    entity_category=EntityCategory.CONFIG,
    native_min_value=30,
    native_max_value=100,
    icon="mdi:fan",
)

FIREPLACE_DELAY = FlexitNumberEntityDescription(
    key="fireplace_ventilation_duration",
    name="Fireplace ventilation duration",
    native_unit_of_measurement=TIME_MINUTES,
    entity_category=EntityCategory.CONFIG,
    native_min_value=0.0,
    native_max_value=300.00,
    icon="mdi:timer",
)
BOOST_DELAY = FlexitNumberEntityDescription(
    key="rapid_ventilation_duration",
    name="Rapid ventilation duration",
    native_unit_of_measurement=TIME_MINUTES,
    entity_category=EntityCategory.CONFIG,
    native_min_value=0.0,
    native_max_value=300.00,
    icon="mdi:timer",
)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Flexit number."""

    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        FlexitSetpointHomeExtractNumber(coordinator, SETPOINT_HOME_EXTRACT),
        FlexitSetpointHomeSupplyNumber(coordinator, SETPOINT_HOME_SUPPLY),
        FlexitSetpointAwayExtractNumber(coordinator, SETPOINT_AWAY_EXTRACT),
        FlexitSetpointAwaySupplyNumber(coordinator, SETPOINT_AWAY_SUPPLY),
        FlexitSetpointHighExtractNumber(coordinator, SETPOINT_HIGH_EXTRACT),
        FlexitSetpointHighSupplyNumber(coordinator, SETPOINT_HIGH_SUPPLY),
        FlexitSetpointFireExtractNumber(coordinator, SETPOINT_FIRE_EXTRACT),
        FlexitSetpointFireSupplyNumber(coordinator, SETPOINT_FIRE_SUPPLY),
        FlexitSetpointCookerExtractNumber(coordinator, SETPOINT_COOKER_EXTRACT),
        FlexitSetpointCookerSupplyNumber(coordinator, SETPOINT_COOKER_SUPPLY),
        FlexitBoostDelayNumber(coordinator, BOOST_DELAY),
        FlexitFireplaceDelayNumber(coordinator, FIREPLACE_DELAY),
    ])

class FlexitNumber(CoordinatorEntity, NumberEntity):
    """Define a Flexit entity."""

    sensor_data: Any
    coordinator: FlexitDataUpdateCoordinator
    entity_description: FlexitNumberEntityDescription

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
        description: FlexitNumberEntityDescription,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entity_description = description
        self._attr_unique_id = f"{description.key}"
        self._attr_device_info = coordinator._attr_device_info

        self._attr_native_step = 1
        self._attr_mode: Literal["auto", "slider", "box"] = MODE_AUTO
        self._attr_native_min_value = description.native_min_value or DEFAULT_MIN_VALUE
        self._attr_native_max_value = description.native_max_value or DEFAULT_MAX_VALUE

    @property
    def available(self) -> bool:
        """Entity is available"""
        return self.coordinator.device.available

    @property
    def native_value(self) -> float:
        return self.coordinator.device.__getattribute__(
            self.entity_description.key
        )

class FlexitSetpointHomeExtractNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_extract_air_home(value)
        self.schedule_update_ha_state()

class FlexitSetpointHomeSupplyNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_home(value)
        self.schedule_update_ha_state()

class FlexitSetpointAwayExtractNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_away(value)
        self.schedule_update_ha_state()

class FlexitSetpointAwaySupplyNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_away(value)
        self.schedule_update_ha_state()

class FlexitSetpointHighExtractNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_high(value)
        self.schedule_update_ha_state()

class FlexitSetpointHighSupplyNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_high(value)
        self.schedule_update_ha_state()

class FlexitSetpointFireExtractNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_fire(value)
        self.schedule_update_ha_state()

class FlexitSetpointFireSupplyNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_fire(value)
        self.schedule_update_ha_state()

class FlexitSetpointCookerExtractNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_cooker(value)
        self.schedule_update_ha_state()

class FlexitSetpointCookerSupplyNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fan_setpoint_supply_air_cooker(value)
        self.schedule_update_ha_state()

class FlexitBoostDelayNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_rapid_ventilation_duration(value)
        self.schedule_update_ha_state()

class FlexitFireplaceDelayNumber(FlexitNumber):
    def set_native_value(self, value: float) -> None:
        self.coordinator.device.set_fireplace_ventilation_duration(int(value))
        self.schedule_update_ha_state()
