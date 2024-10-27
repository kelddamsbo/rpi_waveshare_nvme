# Waveshare PCIe To M.2 Adapter for Raspberry Pi 5

Home Assistant integration for the Waveshare PCIe To M.2 Adapter for Raspberry Pi 5.

## Description

This integration can be used to get information over i2c for the
Waveshare PCIe To M.2 Adapter for the Raspberry Pi 5.
The integration assumes that you have followed the instructions for
enabling i2c on your Raspberry Pi. These instructions will differ
depending on how you are running Home Assistant.

If you are running Home Assistant OS see
[here](https://www.home-assistant.io/common-tasks/os/#enable-i2c).

### Entities Provided

#### Sensors

* __Current__
* __Load Voltage__ - the voltage on V- (load side)
* __Power__
* __PSU Voltage__ - Load Voltage + Shunt Voltage
* __Shunt Voltage__ - voltage between V+ and V- across the shunt

## Setup

### <a id="ManualAdd"></a>`Add Integration` button

Clicking the `Add Integration` button will cause the integration to start
looking for available devices on i2c.

![Initial Setup Screen](images/step_user.png)

Once the detection process has finished the following information will be
required.

![Selection Screen](images/step_select.png)

* __Name__ - friendly name for the configuration entry
* __Address of the HAT__ - if only a single address was found it will be
selected. If multiple addresses are found the first is selected and you'll
need to pick the correct one to use.
* __Version of the HAT__ - defaults to nvme. You should pick the version that you
have.
* __Update interval__ - defaults to 10s. Defines how often to query the UPS.

On successful set up the following screen will be seen detailing the device.

![Final Setup Screen](images/setup_finish.png)

## Configurable Options

It is possible to configure the following options for the integration.

![Configure Options](images/config_options.png)

* __Update interval__ - defaults to 10s. Defines how often to query the UPS.
