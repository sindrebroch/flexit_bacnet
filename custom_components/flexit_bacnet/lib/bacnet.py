import socket

from typing import List, Any
from logging import Logger, getLogger

import BAC0
from BAC0.scripts import Lite
from contextlib import asynccontextmanager

from .device_property import DeviceProperty, PRESENT_VALUE
from .typing import DeviceState

LOGGER: Logger = getLogger(__package__)

BAC0.log_level('silence')

def get_local_ip(device_address: str) -> None | str:
    """Get the local IP address used to connect to the remote one."""
    LOGGER.info("Trying to get_local_ip in bacnet")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((device_address, 0))
    except socket.error:
        return None
    else:
        return s.getsockname()[0]
    finally:
        s.close()

@asynccontextmanager
async def run_bacnet(hass, device_address: str) -> Lite:
    """Return a running BACnet application to accept read and write requests."""
    LOGGER.info("Trying to run_bacnet")

    local_ip = get_local_ip(device_address)
    bacnet_lite = await hass.async_add_executor_job(BAC0.lite, local_ip, None, None, None, 0, None, True)

    try:
        yield bacnet_lite
    except Exception as e:
        LOGGER.warning("run_bacnet exception %s", e)
    finally:
        await hass.async_add_executor_job(bacnet_lite.disconnect)
        LOGGER.info("run_bacnet finally finished")

async def read_multiple(hass, device_address: str, device_properties: List[DeviceProperty]) -> DeviceState:
    LOGGER.info("Trying to read_multiple in bacnet")
    request = {
        'address': device_address,
        'objects': {
            f'{dp.object_type}:{dp.instance_id}': dp.read_values
            for dp in device_properties
        },
    }

    result: DeviceState

    async with run_bacnet(hass, device_address) as bacnet:
        try:
            result = await hass.async_add_executor_job(bacnet.readMultiple, device_address, request)
            LOGGER.debug("response from read %s", result)
        except Exception as e: 
            LOGGER.warning("Error on bacnet.readMultiple, %s", e)

    if result == ['']:
        raise ConnectionError

    return result


async def write(hass, device_address: str, device_property: DeviceProperty, value: Any):
    LOGGER.debug("Trying to write in bacnet")
    async with run_bacnet(hass, device_address) as bacnet:
        args = [
            device_address,
            device_property.object_type,
            device_property.instance_id,
            PRESENT_VALUE,
            value
        ]

        if device_property.priority is not None:
            args += [f'- {device_property.priority}']

        try:
            LOGGER.debug("bacnet.write %s", args)
            result = await hass.async_add_executor_job(bacnet.write, " ".join(map(lambda arg: str(arg), args)) )            
        except Exception as e:
            LOGGER.warning("Error on bacnet.write, %s", e)
