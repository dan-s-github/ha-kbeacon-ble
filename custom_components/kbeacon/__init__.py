"""The KBeacon BLE integration."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.components.bluetooth import BluetoothScanningMode
from homeassistant.components.bluetooth.passive_update_processor import (
    PassiveBluetoothProcessorCoordinator,
)
from homeassistant.const import Platform
from kbeacon_ble import KBeaconBluetoothDeviceData

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

type KBeaconConfigEntry = ConfigEntry[PassiveBluetoothProcessorCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: KBeaconConfigEntry) -> bool:
    """Set up KBeacon BLE device from a config entry."""
    address = entry.unique_id
    if address is None:
        return False
    data = KBeaconBluetoothDeviceData()
    coordinator = entry.runtime_data = PassiveBluetoothProcessorCoordinator(
        hass,
        _LOGGER,
        address=address,
        mode=BluetoothScanningMode.PASSIVE,
        update_method=data.update,
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(
        coordinator.async_start()
    )  # only start after all platforms have had a chance to subscribe
    return True


async def async_unload_entry(hass: HomeAssistant, entry: KBeaconConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
