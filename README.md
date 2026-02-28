# KBeacon BLE

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

Home Assistant integration for KBeacon Bluetooth Low Energy (BLE) devices.

This integration automatically discovers and monitors KBeacon BLE sensors through passive Bluetooth scanning. It supports temperature, humidity, and battery voltage monitoring.

## Features

- **Automatic Discovery**: Automatically detects KBeacon BLE devices in range
- **Passive Scanning**: Uses Bluetooth passive scanning mode for efficient battery usage
- **Multiple Sensor Types**:
  - Temperature (°C)
  - Humidity (%)
  - Battery Voltage (V)
- **No Configuration Required**: Devices are automatically discovered and added through the UI

## Requirements

- Home Assistant 2025.2.4 or newer
- Bluetooth adapter (built-in or USB)
- KBeacon BLE device broadcasting Eddystone telemetry

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/dan-s-github/ha-kbeacon-ble`
6. Select category "Integration"
7. Click "Add"
8. Find "KBeacon BLE" in the integration list and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Extract the `custom_components/kbeacon_ble` directory to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "KBeacon BLE"
4. Select your KBeacon device from the list of discovered devices
5. Click **Submit**

The integration will automatically create sensor entities for:
- Temperature
- Humidity
- Battery Voltage (disabled by default, can be enabled in entity settings)

## Development (Devcontainer + Bluetooth)

- On macOS hosts, the VS Code devcontainer cannot map the host Bluetooth adapter for Home Assistant BLE testing.
- On Linux hosts, Bluetooth passthrough may work with host networking/privileged mode and a D-Bus mount.
- This repository includes the required D-Bus mount in [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json).
- If BLE discovery still does not work in-container, run Home Assistant directly on the host or test on a physical Linux machine.

## Supported Devices

This integration supports KBeacon BLE devices that broadcast Eddystone telemetry data with manufacturer ID 33 (0x21).

## Troubleshooting

### Device Not Discovered

- Ensure your KBeacon device is powered on and in range
- Check that Bluetooth is enabled in Home Assistant
- Verify the device is broadcasting in Eddystone mode
- Try restarting the Bluetooth adapter

### Sensors Not Updating

- Check the device battery level
- Ensure the device is within Bluetooth range
- Review Home Assistant logs for any error messages

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Report a Bug][issues]
- [Request a Feature][issues]
- [Ask a Question][issues]

---

[releases-shield]: https://img.shields.io/github/release/dan-s-github/ha-kbeacon-ble.svg?style=for-the-badge
[releases]: https://github.com/dan-s-github/ha-kbeacon-ble/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/dan-s-github/ha-kbeacon-ble.svg?style=for-the-badge
[commits]: https://github.com/dan-s-github/ha-kbeacon-ble/commits/main
[license-shield]: https://img.shields.io/github/license/dan-s-github/ha-kbeacon-ble.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[issues]: https://github.com/dan-s-github/ha-kbeacon-ble/issues
