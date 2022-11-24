from datetime import timedelta

from .const import DOMAIN, LOGGER

from homeassistant.core import HomeAssistant

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER
from .lib import FlexitBACnet

class FlexitDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching from Flexit data API."""

    def __init__(
            self,
            hass: HomeAssistant,
            name: str,
            device: FlexitBACnet
    ) -> None:
        """Initialize."""

        self.name = name
        self.device = device

        self._attr_device_info = DeviceInfo(
            name=self.name,
            manufacturer="Flexit Bacnet",
            model=self.device.device_name,
            identifiers={(DOMAIN, self.device.serial_number)},
        )

        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5)
        )

    async def _async_update_data(self):
        """Update data via library."""
        self.device.refresh()
