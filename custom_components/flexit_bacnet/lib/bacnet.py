import socket
import asyncio

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
        LOGGER.debug("Try socket")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        LOGGER.debug("Try socket 2")
        s.connect((device_address, 0))
        LOGGER.debug("Try socket 3")
    except socket.error as e:
        LOGGER.warning("Socket error %s", e)
        return None
    except Exception as e:
        LOGGER.warning("Socket exception %s", e)
    else:
        LOGGER.debug("Socket return")
        return s.getsockname()[0]
    finally:
        LOGGER.debug("Socket close")
        s.close()

@asynccontextmanager
async def run_bacnet(hass, device_address: str) -> Lite:
    """Return a running BACnet application to accept read and write requests."""
    LOGGER.debug("Trying to run_bacnet")

    try:
        LOGGER.debug("Get local_ip")
        local_ip = await hass.async_add_executor_job(get_local_ip, device_address)
        async with asyncio.timeout(10):
            LOGGER.debug("Get bacnet_lite")
            bacnet_lite = await hass.async_add_executor_job(BAC0.lite, local_ip, None, None, None, 0, None, True)
        LOGGER.debug("Yield bacnet_lite")
        yield bacnet_lite
    except TimeoutError as e:
        LOGGER.warning("run_bacnet timeout error %s", e)
    except Exception as e:
        LOGGER.warning("run_bacnet exception %s", e)
    finally:
        if bacnet_lite is not None:
            LOGGER.debug("run_bacnet finally disconnect")
            await hass.async_add_executor_job(bacnet_lite.disconnect)
        LOGGER.debug("run_bacnet finally finished")

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
