
from typing import Any, cast

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, TEMP_CELSIUS, REVOLUTIONS_PER_MINUTE, TIME_HOURS, TIME_MINUTES, ENERGY_KILO_WATT_HOUR
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
        name="Comfort button",
        key="comfort_button",
    ),
    SensorEntityDescription(
        name="Operation mode",
        key="operation_mode",
    ),
    SensorEntityDescription(
        name="Ventilation mode",
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
        name="Air temp setpoint away",
        key="air_temp_setpoint_away",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        name="Air temp setpoint home",
        key="air_temp_setpoint_home",
        icon=TEMPERATURE_ICON,
        native_unit_of_measurement=TEMP_CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    SensorEntityDescription(
        name="Fan setpoint supply air home",
        key="fan_setpoint_supply_air_home",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint extract air home",
        key="fan_setpoint_extract_air_home",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),

    SensorEntityDescription(
        name="Fireplace ventilation remaining duration",
        key="fireplace_ventilation_remaining_duration",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TIME_MINUTES,
    ),
    SensorEntityDescription(
        name="Rapid ventilation remaining duration",
        key="rapid_ventilation_remaining_duration",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=TIME_MINUTES,
    ),
    SensorEntityDescription(
        name="Fan Control Signal Supply",
        key="supply_air_fan_control_signal",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan speed supply",
        key="supply_air_fan_rpm",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
    ),
    SensorEntityDescription(
        name="Fan Control Signal Exhaust",
        key="exhaust_air_fan_control_signal",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan speed exhaust",
        key="exhaust_air_fan_rpm",
        icon=FAN_ICON,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
    ),
    SensorEntityDescription(
        name="Electric heater",
        icon=HEATING_ICON,
        key="electric_heater",
    ),
    SensorEntityDescription(
        name="Electric heater nominal power",
        key="electric_heater_nominal_power",
        device_class=SensorDeviceClass.POWER,
        icon=HEATING_ICON,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        name="Electric heater power",
        key="electric_heater_power",
        icon=HEATING_ICON,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        name="Fan setpoint supply air high",
        key="fan_setpoint_supply_air_high",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint extract air high",
        key="fan_setpoint_extract_air_high",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint supply air away",
        key="fan_setpoint_supply_air_away",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint extract air away",
        key="fan_setpoint_extract_air_away",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint supply air cooker",
        key="fan_setpoint_supply_air_cooker",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint extract air cooker",
        key="fan_setpoint_extract_air_cooker",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint supply air fire",
        key="fan_setpoint_supply_air_fire",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
    ),
    SensorEntityDescription(
        name="Fan setpoint extract air fire",
        key="fan_setpoint_extract_air_fire",
        icon=FAN_ICON,
        native_unit_of_measurement=PERCENTAGE,
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
        name="Scheduler override",
        key="scheduler_override",
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
    def native_value(self) -> StateType:
        sensor_data = self.coordinator.device.__getattribute__(self.entity_description.key)
        return cast(StateType, sensor_data)
