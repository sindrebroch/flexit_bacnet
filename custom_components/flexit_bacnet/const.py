from logging import Logger, getLogger
from typing import List

from homeassistant.const import Platform

DOMAIN = "flexit_bacnet"

LOGGER: Logger = getLogger(__package__)

CONF_ADDRESS="address"
CONF_DEVICE_ID="device_id"
CONF_INTERVAL="update_interval"

DEFAULT_INTERVAL = 5

PLATFORMS: List[str] = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]