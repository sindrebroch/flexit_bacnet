
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

SENSORS = [
    SensorEntityDescription(
        name="Outside air temperature",
        key="outside_air_temperature"
    ),
    SensorEntityDescription(
        name="Supply air temperature",
        key="supply_air_temperature"
    ),
    SensorEntityDescription(
        name="Exhaust air temperature",
        key="exhaust_air_temperature"
    ),
    SensorEntityDescription(
        name="Extract air temperature",
        key="extract_air_temperature"
    ),
    SensorEntityDescription(
        name="Room temperature",
        key="room_temperature"
    ),
    SensorEntityDescription(
        name="operation_mode",
        key="operation_mode"
    ),
    SensorEntityDescription(
        name="ventilation_mode",
        key="ventilation_mode"
    ),

    SensorEntityDescription(
        name="air_temp_setpoint_away",
        key="air_temp_setpoint_away"
    ),
    SensorEntityDescription(
        name="air_temp_setpoint_home",
        key="air_temp_setpoint_home"
    ),

    SensorEntityDescription(
        name="fireplace_ventilation_remaining_duration",
        key="fireplace_ventilation_remaining_duration"
    ),
    SensorEntityDescription(
        name="rapid_ventilation_remaining_duration",
        key="rapid_ventilation_remaining_duration"
    ),
    SensorEntityDescription(
        name="supply_air_fan_control_signal",
        key="supply_air_fan_control_signal"
    ),
    SensorEntityDescription(
        name="supply_air_fan_rpm",
        key="supply_air_fan_rpm"
    ),
    SensorEntityDescription(
        name="exhaust_air_fan_control_signal",
        key="exhaust_air_fan_control_signal"
    ),
    SensorEntityDescription(
        name="exhaust_air_fan_rpm",
        key="exhaust_air_fan_rpm"
    ),

    SensorEntityDescription(
        name="electric_heater",
        key="electric_heater"
    ),
    SensorEntityDescription(
        name="electric_heater_nominal_power",
        key="electric_heater_nominal_power"
    ),
    SensorEntityDescription(
        name="electric_heater_power",
        key="electric_heater_power"
    ),
    SensorEntityDescription(
        name="fan_setpoint_supply_air_home",
        key="fan_setpoint_supply_air_home"
    ),
    SensorEntityDescription(
        name="fan_setpoint_extract_air_home",
        key="fan_setpoint_extract_air_home"
    ),
    SensorEntityDescription(
        name="fan_setpoint_supply_air_high",
        key="fan_setpoint_supply_air_high"
    ),
    SensorEntityDescription(
        name="fan_setpoint_extract_air_high",
        key="fan_setpoint_extract_air_high"
    ),
    SensorEntityDescription(
        name="fan_setpoint_supply_air_away",
        key="fan_setpoint_supply_air_away"
    ),
    SensorEntityDescription(
        name="fan_setpoint_extract_air_away",
        key="fan_setpoint_extract_air_away"
    ),
    SensorEntityDescription(
        name="fan_setpoint_supply_air_cooker",
        key="fan_setpoint_supply_air_cooker"
    ),
    SensorEntityDescription(
        name="fan_setpoint_extract_air_cooker",
        key="fan_setpoint_extract_air_cooker"
    ),
    SensorEntityDescription(
        name="fan_setpoint_supply_air_fire",
        key="fan_setpoint_supply_air_fire"
    ),
    SensorEntityDescription(
        name="fan_setpoint_extract_air_fire",
        key="fan_setpoint_extract_air_fire"
    ),
    SensorEntityDescription(
        name="air_filter_operating_time",
        key="air_filter_operating_time"
    ),
    SensorEntityDescription(
        name="air_filter_exchange_interval",
        key="air_filter_exchange_interval"
    ),
    SensorEntityDescription(
        name="heat_exchanger_efficiency",
        key="heat_exchanger_efficiency"
    ),
    SensorEntityDescription(
        name="heat_exchanger_speed",
        key="heat_exchanger_speed"
    ),
    SensorEntityDescription(
        name="air_filter_polluted",
        key="air_filter_polluted"
    ),


]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(FlexitSensor(coordinator, desc) for desc in SENSORS)

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
        return self.coordinator.device.__getattribute__(self.entity_description.key)
