# Flexit BACnet for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/flexit_bacnet?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

This library allows integration with Flexit Nordic series of air handling units via BACnet protocol.

Work in progress.Use at your own risk.

This custom integration is based on the awesome work of the official "Flexit BACnet"-integration from the PR to HA core [here](https://github.com/home-assistant/core/pull/79652). I have extracted the library into the custom_component to experiment and try to expand upon the existing work. Among other changes this integration tries to add async where possible, to avoid blocking the event-loop, but it is difficult since the underlying library BAC0 is not async.

## Prerequisites

In order to use that library, you need to know the IP address and Device ID of your unit.

1. Open Flexit Go app on your mobile.
2. Use "Find product" button on tha main screen.
3. Select your device and press "Connect".
4. Enter installer code (default: 1000) and press "Login".
5. Open "More" menu -> Installer -> Communication -> BACnet settings.
6. Note down "IP address" and "Device ID".

## Installation

<details>
  <summary>HACS (Recommanded)</summary>

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "Flexit Bacnet" integration.
4. Restart Home Assistant.
5. Add the `Flexit Bacnet` integration to HA from the integration-page
6. Enter your IP address and DeviceID
</details>

<details>
  <summary>Manual installation</summary>

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/flexit_bacnet/releases/latest).
2. Unpack the release and copy the `custom_components/flexit_bacnet` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add the `Flexit Bacnet` integration to HA from the integration-page
6. Enter your IP address and DeviceID
</details>

## Features

### Climate-entity

- Preset modes:
  - Home
  - Away
  - Boost
- Operation modes:
  - Fan only
  - Heat
  - Off
- Aux heat on / off
- Viewable modes:
  - Home
  - Away
  - Boost

### Sensor-entities

- Electric heater nominal power
- Electric heater power
- Heat exchanger efficiency
- Heat exchanger speed

- Extract Fan Control Signal
- Extract Fan Speed
- Supply Fan Control Signal
- Supply Fan Speed

- Temperature Extract
- Temperature Exhaust
- Temperature Outside
- Temperature Supply
- Temperature Room

- Fireplace remaining duration
- Rapid ventilation remaining duration

- Mode operation
- Mode ventilation

### Number-entities

- Extract / Supply Fan setpoint for all modes
- Fireplace remaining duration
- Rapid ventilation remaining duration

### Switch-entities

- Comfort button
- Scheduler override

### Binary sensor-entities

- Dirty filter
  - Hours since change
  - Hours until dirty
  - Filter change interval hours
  - Days since change
  - Days until dirty
  - Filter change interval days

### Button-entities

- Activate / Deactivate Cooker hood

## Debugging

If something is not working properly, logs might help with debugging. To turn on debug-logging add this to your `configuration.yaml`

```
logger:
  default: info
  logs:
    custom_components.flexit_bacnet: debug
```
