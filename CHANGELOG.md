## v1.0.0rc0 (2026-04-26)

### Feat

- fix lint violations across integration and tests
- **sensor**: set voltage sensor display precision to 3 decimals
- add UID tx power diagnostic sensor
- add battery, CO2, and illuminance sensor support

### Fix

- address PR review comments
- correct mypy key cast for sensor descriptions
- satisfy mypy typing for sensor description lookup
- align HA 2026.3 deps and restore integration tests
- **manifest**: use KBeacon-specific 2080 service_data_uuid for BLE discovery
- **hacs**: name needs to reflect custom_components folder
- resolve CI validation errors and workflow issues

### Refactor

- align infrastructure with ha-jaalee-ble template
- rename Home Assistant integration package to kbeacon
