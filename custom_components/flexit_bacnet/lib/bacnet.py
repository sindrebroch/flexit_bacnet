import socket
from typing import List, Any
from logging import Logger, getLogger

import BAC0
from BAC0.scripts import Lite
from decorator import contextmanager

from .device_property import DeviceProperty, PRESENT_VALUE
from .typing import DeviceState

LOGGER: Logger = getLogger(__package__)

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

@contextmanager
def run_bacnet(device_address: str) -> Lite:
    """Return a running BACnet application to accept read and write requests."""
    LOGGER.info("Trying to run_bacnet")

    try:
        bacnet_lite = BAC0.lite(ip=get_local_ip(device_address), ping=False)
        yield bacnet_lite
    finally:
        LOGGER.info("run_bacnet finally")
        bacnet_lite.disconnect()

def disconnect(device_address: str):
    LOGGER.info("Trying to disconnect bacnet")
    with run_bacnet(device_address) as bacnet:
        bacnet.disconnect()
        LOGGER.info("Have called bacnet.disconnect()")


def read_multiple(device_address: str, device_properties: List[DeviceProperty]) -> DeviceState:
    LOGGER.info("Trying to read_multiple in bacnet")
    request = {
        'address': device_address,
        'objects': {
            f'{dp.object_type}:{dp.instance_id}': dp.read_values
            for dp in device_properties
        },
    }

    result: DeviceState

    with run_bacnet(device_address) as bacnet:
        try:
            result = bacnet.readMultiple(device_address, request)
        except:
            LOGGER.info("error on readMultiple")

    if result == ['']:
        raise ConnectionError

    return result


def write(device_address: str, device_property: DeviceProperty, value: Any):
    LOGGER.info("Trying to write in bacnet")
    with run_bacnet(device_address) as bacnet:
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
            bacnet.write(" ".join(map(lambda arg: str(arg), args)))
        except:
            LOGGER.info("error onwrite")
