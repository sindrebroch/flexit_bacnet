"""The Flexit Nordic (BACnet) integration."""
from typing import Any

from .lib import VENTILATION_MODE
from .lib.nordic import VENTILATION_MODES

from homeassistant.components.climate import (
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_HOME,
    PRESET_NONE,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import FlexitDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Honeywell thermostat."""
    coordinator: FlexitDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([FlexitClimateEntity(coordinator)])


class FlexitClimateEntity(ClimateEntity):
    """Flexit air handling unit."""

    coordinator: FlexitDataUpdateCoordinator

    _attr_supported_features = (
        ClimateEntityFeature.PRESET_MODE
        | ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.AUX_HEAT
    )

    _attr_hvac_modes = [
        HVACMode.OFF,
        HVACMode.HEAT,
        HVACMode.FAN_ONLY,
    ]

    _attr_preset_modes = [
        PRESET_AWAY,
        PRESET_HOME,
        PRESET_BOOST,
    ]

    _attr_temperature_unit = TEMP_CELSIUS
    _attr_target_temperature_step = 1.0
    _attr_has_entity_name = True
    _attr_icon = "mdi:hvac"

    def __init__(
        self,
        coordinator: FlexitDataUpdateCoordinator,
    ) -> None:
        """Initialize the unit."""
        self.coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}.{self.coordinator.device.serial_number}"
        self._attr_device_info = coordinator._attr_device_info

    def update(self) -> None:
        """Refresh unit state."""
        self.coordinator.device.refresh()

    @property
    def name(self) -> str:
        """Name of the entity."""
        return f"Flexit Nordic: {self.coordinator.device.serial_number}"

    @property
    def available(self) -> bool:
        """Entity is available"""
        return self.coordinator.device.available

    @property
    def current_temperature(self) -> float:
        """Return the current temperature."""
        return float(self.coordinator.device.room_temperature)

    @property
    def target_temperature(self) -> float:
        """Return the temperature we try to reach."""
        if self.coordinator.device.ventilation_mode == VENTILATION_MODES[VENTILATION_MODE.AWAY]:
            return float(self.coordinator.device.air_temp_setpoint_away)

        return float(self.coordinator.device.air_temp_setpoint_home)

    def set_temperature(self, **kwargs: Any) -> None:
        """Set new target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return

        if self.coordinator.device.ventilation_mode == VENTILATION_MODES[VENTILATION_MODE.AWAY]:
            self.coordinator.device.set_air_temp_setpoint_away(temperature)
        else:
            self.coordinator.device.set_air_temp_setpoint_home(temperature)
        self.update()

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode, e.g., home, away, temp.
        Requires ClimateEntityFeature.PRESET_MODE.
        """
        return {
            VENTILATION_MODES[VENTILATION_MODE.STOP]: PRESET_NONE,
            VENTILATION_MODES[VENTILATION_MODE.AWAY]: PRESET_AWAY,
            VENTILATION_MODES[VENTILATION_MODE.HOME]: PRESET_HOME,
            VENTILATION_MODES[VENTILATION_MODE.HIGH]: PRESET_BOOST,
        }[self.coordinator.device.ventilation_mode]

    def set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        ventilation_mode = {
            PRESET_NONE: VENTILATION_MODE.STOP,
            PRESET_AWAY: VENTILATION_MODE.AWAY,
            PRESET_HOME: VENTILATION_MODE.HOME,
            PRESET_BOOST: VENTILATION_MODE.HIGH,
        }[preset_mode]

        self.coordinator.device.set_ventilation_mode(ventilation_mode)
        self.update()

    @property
    def hvac_mode(self) -> HVACMode:
        """Return hvac operation ie. heat, cool mode."""
        if self.coordinator.device.ventilation_mode == VENTILATION_MODES[VENTILATION_MODE.STOP]:
            return HVACMode.OFF

        if self.is_aux_heat:
            return HVACMode.HEAT

        return HVACMode.FAN_ONLY

    def set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target hvac mode."""
        if hvac_mode == HVACMode.OFF:
            self.coordinator.device.set_ventilation_mode(VENTILATION_MODE.STOP)
        else:
            self.coordinator.device.set_ventilation_mode(VENTILATION_MODE.HOME)

        if hvac_mode == HVACMode.HEAT:
            self.turn_aux_heat_on()
        else:
            self.turn_aux_heat_off()
        self.update()

    @property
    def is_aux_heat(self) -> bool:
        """Return true if aux heater.
        Requires ClimateEntityFeature.AUX_HEAT.
        """
        return bool(self.coordinator.device.electric_heater)

    def turn_aux_heat_on(self) -> None:
        """Turn auxiliary heater on."""
        self.coordinator.device.enable_electric_heater()
        self.update()

    def turn_aux_heat_off(self) -> None:
        """Turn auxiliary heater off."""
        self.coordinator.device.disable_electric_heater()
        self.update()
