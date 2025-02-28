
from typing import Any, cast

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS, REVOLUTIONS_PER_MINUTE, TIME_HOURS, TIME_MINUTES, POWER_KILO_WATT
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .coordinator import FlexitDataUpdateCoordinator

TEMPERATURE_ICON = "mdi:thermometer"
FAN_ICON = "mdi:fan"
HEATING_ICON = "mdi:radiator"

SENSORS = [
    SensorEntityDescription(
        name="Mode Operation",
        key="operation_mode",
    ),
    SensorEntityDescription(
        name="Mode Ventilation",
        key="ventilation_mode",
    ),

    SensorEntityDescription(
        name="Temperature Outside",
        key="outside_air_temperature",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Temperature Supply",
        key="supply_air_temperature",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Temperature Exhaust",
        key="exhaust_air_temperature",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Temperature Extract",
        key="extract_air_temperature",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Temperature Room",
        key="room_temperature",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Supply Fan Control Signal",
        key="supply_air_fan_control_signal",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Supply Fan Speed",
        key="supply_air_fan_rpm",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
    ),
    SensorEntityDescription(
        name="Exhaust Fan Control Signal",
        key="exhaust_air_fan_control_signal",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Exhaust Fan Speed",
        key="exhaust_air_fan_rpm",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
    ),
    SensorEntityDescription(
        name="Electric heater nominal power",
        key="electric_heater_nominal_power",
        device_class=SensorDeviceClass.POWER,
        icon=HEATING_ICON,
        native_unit_of_measurement=POWER_KILO_WATT,
    ),
    SensorEntityDescription(
        name="Electric heater power",
        key="electric_heater_power",
        icon=HEATING_ICON,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=POWER_KILO_WATT,
    ),

    SensorEntityDescription(
        name="Heat exchanger efficiency",
        key="heat_exchanger_efficiency",
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Heat exchanger speed",
        key="heat_exchanger_speed",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),

    SensorEntityDescription(
        name="Fireplace ventilation remaining duration",
        key="fireplace_ventilation_remaining_duration",
    ),
    SensorEntityDescription(
        name="Rapid ventilation remaining duration",
        key="rapid_ventilation_remaining_duration",
    ),
]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        FlexitSensor(coordinator, description)
        for description in SENSORS
    )

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

    @property
    def available(self) -> bool:
        """Entity is available"""
        return self.coordinator.device.available

    @property
    def native_value(self) -> StateType:
        sensor_data = self.coordinator.device.__getattribute__(self.entity_description.key)
        return cast(StateType, sensor_data)
