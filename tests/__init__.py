"""Tests for the KBeacon BLE integration."""

from uuid import UUID

from bleak.backends.device import BLEDevice
from bluetooth_data_tools import monotonic_time_coarse
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak


def make_bluetooth_service_info(
    name: str,
    manufacturer_data: dict[int, bytes],
    service_uuids: list[str],
    address: str,
    rssi: int,
    service_data: dict[str, bytes],
    source: str,
    tx_power: int = 0,
) -> BluetoothServiceInfoBleak:
    """Create a BluetoothServiceInfoBleak object for testing."""
    return BluetoothServiceInfoBleak(
        name=name,
        manufacturer_data=manufacturer_data,
        service_uuids=service_uuids,
        address=address,
        rssi=rssi,
        service_data={UUID(k): v for k, v in service_data.items()},
        source=source,
        device=BLEDevice(
            name=name,
            address=address,
            details={},
        ),
        time=monotonic_time_coarse(),
        advertisement=None,
        connectable=True,
        tx_power=tx_power,
    )


NOT_KBEACON_SERVICE_INFO = make_bluetooth_service_info(
    name="Not it",
    address="61DE521B-F0BF-9F44-64D4-75BBE1738105",
    rssi=-63,
    manufacturer_data={3234: b"\x00\x01"},
    service_data={},
    service_uuids=[],
    source="local",
)

# Sample payload from kbeacon-ble library tests:
# "2101070e321b4733b4"
# - Frame type: 0x21
# - Sensor mask: 0x0107 (bits 0,1,2 set - voltage, temperature, humidity)
# - Voltage: 0x0E32 = 3634 mV -> 3.634 V
# - Temperature: 0x1B47 = 6983 -> 27.28 C
# - Humidity: 0x33B4 = 13236 -> 51.7%
KBEACON_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_142081",
    address="BC:57:29:02:45:9F",
    rssi=-60,
    service_data={
        "0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex("2101070e321b4733b4")
    },
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# Test data with only voltage
KBEACON_VOLTAGE_ONLY_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_Test",
    address="BC:57:29:02:45:A0",
    rssi=-60,
    service_data={"0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex("2100010BB8")},
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# Test data with negative temperature
KBEACON_NEGATIVE_TEMP_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_Freezer",
    address="BC:57:29:02:45:A1",
    rssi=-60,
    service_data={"0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex("210002F600")},
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# Test data with FEAA light and CO2 fields
KBEACON_LUX_CO2_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_CO2",
    address="BC:57:29:02:45:A2",
    rssi=-60,
    service_data={
        "0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex(
            "2102470E101A003200012C0503E8"
        )
    },
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# Test data with FEAA system frame (0x22) battery field
KBEACON_SYSTEM_BATTERY_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_System",
    address="BC:57:29:02:45:A3",
    rssi=-60,
    service_data={
        "0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex("220161BC57290245A30102")
    },
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)

# Test data with FEAA UID frame (0x00) Tx power field
KBEACON_UID_TX_POWER_SERVICE_INFO = make_bluetooth_service_info(
    name="KBPro_UID",
    address="BC:57:29:02:45:A4",
    rssi=-60,
    service_data={
        "0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex(
            "00F4000000000000000000000000000000000000"
        )
    },
    manufacturer_data={},
    service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
    source="local",
)
