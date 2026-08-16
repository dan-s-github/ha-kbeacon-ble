# KBeacon BLE

[![HACS][hacsbadge]][hacs]
[![GitHub Release][releases-shield]][releases]
[![Integration Usage][downloads-shield]][downloads]

[![Home Assistant][ha-shield]][ha]
[![Python Version][python-shield]][python]
[![License][license-shield]](LICENSE)

[![Tests][tests-shield]][tests]
[![Code Style: Ruff][ruff-shield]][ruff]
[![GitHub Activity][commits-shield]][commits]

Home Assistant integration for KBeacon Bluetooth Low Energy (BLE) devices.

This integration automatically discovers and monitors KBeacon BLE sensors through passive Bluetooth scanning. It supports temperature, humidity, battery percentage, battery voltage, illuminance, CO2, acceleration, and diagnostic monitoring (UID Tx power, unread record count, and other beacon status fields).

## Features

- **Automatic Discovery**: Automatically detects KBeacon BLE devices in range
- **Passive Scanning**: Uses Bluetooth passive scanning mode for efficient battery usage
- **Multiple Sensor Types**:
  - Temperature (°C)
  - Humidity (%)
  - Battery (%)
  - Battery Voltage (V)
  - Illuminance (lux)
  - CO2 (ppm)
  - Acceleration X/Y/Z (m/s²)
  - UID Tx Power (dBm, diagnostic)
  - Unread Records (diagnostic)
  - Unread Records Flags (diagnostic, disabled by default)
  - Sensor Reserved Field (diagnostic, disabled by default)
  - Sensor Tick Counter (diagnostic, disabled by default)
- **No YAML Configuration Required**: Devices are discovered through Bluetooth and added with the UI flow

## Requirements

- Home Assistant 2026.7.0 or newer
- Python 3.14.2 or newer
- Bluetooth adapter (built-in or USB)
- KBeacon BLE device broadcasting Eddystone telemetry

## Installation

### HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dan-s-github&repository=ha-kbeacon-ble&category=Integration)

"Download" and Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page][releases]
2. Extract the `custom_components/kbeacon` directory to your Home Assistant's `custom_components` directory
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
- Battery
- Battery Voltage (disabled by default, can be enabled in entity settings)
- Illuminance
- CO2
- Acceleration X/Y/Z
- UID Tx Power (disabled by default, can be enabled in entity settings)
- Unread Records
- Unread Records Flags (disabled by default, can be enabled in entity settings)
- Sensor Reserved Field (disabled by default, can be enabled in entity settings)
- Sensor Tick Counter (disabled by default, can be enabled in entity settings)

Entities only appear for values the device actually broadcasts — for example, illuminance, CO2, and acceleration entities are only created once those values are first seen in advertisements from the device.

## Development (Devcontainer + Bluetooth)

- Run `scripts/setup` once after cloning. It installs dependencies and links `config/custom_components` to the repository `custom_components` directory.
- Start Home Assistant with `scripts/develop`.
- Optional direct command: `uv run --group dev hass --config config --debug`.
- Run tests with `uv run --group dev pytest`.
- Run type checks with `uv run --group dev mypy custom_components`.
- Run all pre-commit checks with `pre-commit run --all-files`.
- Dependency policy: pin the Home Assistant version we target and rely on its dependency set for transitive packages; avoid manually pinning Home Assistant internals unless there is a documented compatibility break.
- Keep `pycares>=5.0.0,<6` in the dev dependency group; Home Assistant 2026.7.0 requires pycares 5.x.
- On macOS hosts, the VS Code devcontainer cannot map the host Bluetooth adapter for Home Assistant BLE testing.
- On Linux hosts, configure the devcontainer with `--network=host`, `--cap-add=NET_ADMIN`, and `--cap-add=NET_RAW`; these capabilities are required for Home Assistant Bluetooth adapter management and automatic adapter recovery.
- On Linux hosts, mount D-Bus (`/run/dbus`) into the devcontainer if you need full adapter introspection and control.
- On Linux hosts, Bluetooth passthrough may work with host networking/privileged mode and a D-Bus mount.
- If BLE discovery still does not work in-container, run Home Assistant directly on the host or test on a physical Linux machine.

## Supported Devices

This integration supports KBeacon BLE devices that broadcast Eddystone telemetry data with manufacturer ID 33 (0x21).

KBPro and PU200 devices are identified using the Eddystone service UUID (`0xFEAA`), which is a generic identifier shared by many Bluetooth beacon products, not just KBeacon devices. To avoid matching unrelated Eddystone beacons, discovery for these devices is additionally restricted by advertised name (`KBPro*`, `PU200*`).

## Troubleshooting

### Device Not Discovered

- Ensure your KBeacon device is powered on and in range
- Check that Bluetooth is enabled in Home Assistant
- Verify the device is broadcasting in Eddystone mode
- Try restarting the Bluetooth adapter
- KBPro and PU200 devices are matched by advertised name (`KBPro*`, `PU200*`), and that name is only present in the scan response, not the primary advertisement. If you're discovering these devices through a Bluetooth proxy (e.g. ESPHome), set `active: true` on the proxy so it requests scan response data. Passive-only proxies will never see the name and won't trigger initial discovery. Once the device is added, subsequent tracking does not require active scanning.

### Sensors Not Updating

- Check the device battery level
- Ensure the device is within Bluetooth range
- Review Home Assistant logs for any error messages

### Bluetooth Recovery Warnings In Development

If you see warnings such as `Operation not permitted` from `bluetooth_auto_recovery.recover`, Home Assistant can usually still scan, but it cannot power-cycle the adapter for recovery.

- In a devcontainer, ensure `--network=host`, `--cap-add=NET_ADMIN`, and `--cap-add=NET_RAW` are active, then rebuild/reopen the container.
- Mount D-Bus (`/run/dbus`) into the container when testing Bluetooth recovery behavior.
- If you run Home Assistant directly on Linux host, run `sudo scripts/enable-bt-caps` once to grant Bluetooth management capabilities to the interpreter used by this project venv.
- To roll back host capability changes, run `sudo scripts/disable-bt-caps`.

If logs mention `passive scanning on Linux requires BlueZ >= 5.56 with --experimental enabled`, verify `bluetoothd` is started with `--experimental`.

- Check current service command: `systemctl show bluetooth -p ExecStart --value`
- If `--experimental` is missing, run `sudo systemctl edit bluetooth` and add:
  - `[Service]`
  - `ExecStart=`
  - `ExecStart=/usr/libexec/bluetooth/bluetoothd --experimental`
- Apply with `sudo systemctl daemon-reload && sudo systemctl restart bluetooth`

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- [Report a Bug][issues]
- [Request a Feature][issues]
- [Ask a Question][issues]

---

[releases-shield]: https://img.shields.io/github/release/dan-s-github/ha-kbeacon-ble.svg?style=flat&logo=github
[releases]: https://github.com/dan-s-github/ha-kbeacon-ble/releases
[downloads-shield]: https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=%24.kbeacon_ble.total
[downloads]: https://analytics.home-assistant.io/custom_integrations/kbeacon_ble
[commits-shield]: https://img.shields.io/github/commit-activity/y/dan-s-github/ha-kbeacon-ble.svg?style=flat&logo=github
[commits]: https://github.com/dan-s-github/ha-kbeacon-ble/commits/main
[license-shield]: https://img.shields.io/github/license/dan-s-github/ha-kbeacon-ble.svg?style=flat
[python-shield]: https://img.shields.io/badge/python-3.14.2+-blue.svg?style=flat&logo=python&logoColor=white
[python]: https://www.python.org/
[ha-shield]: https://img.shields.io/badge/Home%20Assistant-2026.7.0+-blue.svg?style=flat&logo=homeassistant&logoColor=white
[ha]: https://www.home-assistant.io/
[tests-shield]: https://img.shields.io/github/actions/workflow/status/dan-s-github/ha-kbeacon-ble/ci.yml?branch=main&style=flat&logo=github
[tests]: https://github.com/dan-s-github/ha-kbeacon-ble/actions/workflows/ci.yml
[ruff-shield]: https://img.shields.io/badge/code%20style-ruff-000000.svg?style=flat&logo=ruff&logoColor=white
[ruff]: https://github.com/astral-sh/ruff
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=flat&logo=homeassistant&logoColor=white
[issues]: https://github.com/dan-s-github/ha-kbeacon-ble/issues
