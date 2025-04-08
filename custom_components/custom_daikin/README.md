# Custom Daikin Integration for Home Assistant

This is a custom integration for Daikin air conditioners that supports devices with firmware version 2.8.0.

## Features

- Support for all Daikin WiFi modules:
  * BRP069Axx/BRP069Bxx/BRP072Axx
  * BRP15B61 aka. AirBase (similar protocol as BRP069Axx)
  * BRP072B/Cxx (needs https access and a key)
  * SKYFi (different protocol, have a password)
  * BRP devices with firmware version 2.8.0

## Installation

### HACS

1. Add this repository to HACS as a custom repository
2. Install the integration through HACS
3. Restart Home Assistant
4. Add the integration through the Home Assistant UI

### Manual

1. Copy the `custom_daikin` directory to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the Home Assistant UI

## Configuration

The integration can be configured through the Home Assistant UI. You will need to provide:

- Host: The IP address of your Daikin device
- Password: (Optional) For SkyFi devices
- Key: (Optional) For BRP072C devices
- UUID: (Optional) For BRP072C devices

## Credits

This integration is based on the [pydaikin](https://github.com/fredrike/pydaikin) library by Fredrik Erlandsson.