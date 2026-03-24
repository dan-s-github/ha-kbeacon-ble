"""Test the KBeacon BLE sensors."""

import pytest

from homeassistant.components.bluetooth import async_get_advertisement_callback
from homeassistant.components.sensor import ATTR_STATE_CLASS
from homeassistant.const import (
    ATTR_FRIENDLY_NAME,
    ATTR_UNIT_OF_MEASUREMENT,
    CONCENTRATION_PARTS_PER_MILLION,
    LIGHT_LUX,
    PERCENTAGE,
    UnitOfElectricPotential,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kbeacon.const import DOMAIN

from . import (
    KBEACON_LUX_CO2_SERVICE_INFO,
    KBEACON_NEGATIVE_TEMP_SERVICE_INFO,
    KBEACON_SERVICE_INFO,
    KBEACON_SYSTEM_BATTERY_SERVICE_INFO,
    KBEACON_UID_TX_POWER_SERVICE_INFO,
    KBEACON_VOLTAGE_ONLY_SERVICE_INFO,
)


def inject_bluetooth_service_info(
    hass: HomeAssistant,
    service_info,
) -> None:
    """Inject bluetooth service info into Home Assistant's bluetooth manager."""
    async_get_advertisement_callback(hass)(service_info)


def enable_entity(hass: HomeAssistant, entity_id: str) -> None:
    """Enable a disabled entity in the entity registry."""
    entity_registry = er.async_get(hass)
    entity_registry.async_update_entity(entity_id, disabled_by=None)


async def reload_entry(hass: HomeAssistant, entry: MockConfigEntry) -> None:
    """Reload a config entry and wait for tasks to settle."""
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()


@pytest.fixture(autouse=True)
def expected_lingering_timers() -> bool:
    """Allow known bluetooth manager timer during sensor tests."""
    return True


async def test_sensors(hass: HomeAssistant) -> None:
    """Test setting up creates the sensors."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:9F",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0
    inject_bluetooth_service_info(hass, KBEACON_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 2

    enable_entity(hass, "sensor.kbeacon_459f_voltage")
    await reload_entry(hass, entry)
    inject_bluetooth_service_info(hass, KBEACON_SERVICE_INFO)
    await hass.async_block_till_done()
    assert len(hass.states.async_all("sensor")) == 3

    temp_sensor = hass.states.get("sensor.kbeacon_459f_temperature")
    temp_sensor_attrs = temp_sensor.attributes
    assert temp_sensor.state == "27.28"
    assert temp_sensor_attrs[ATTR_FRIENDLY_NAME] == "KBeacon 459F Temperature"
    assert temp_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == UnitOfTemperature.CELSIUS
    assert temp_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    humid_sensor = hass.states.get("sensor.kbeacon_459f_humidity")
    humid_sensor_attrs = humid_sensor.attributes
    assert humid_sensor.state == "51.7"
    assert humid_sensor_attrs[ATTR_FRIENDLY_NAME] == "KBeacon 459F Humidity"
    assert humid_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE
    assert humid_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    voltage_sensor = hass.states.get("sensor.kbeacon_459f_voltage")
    voltage_sensor_attrs = voltage_sensor.attributes
    assert voltage_sensor.state == "3.634"
    assert voltage_sensor_attrs[ATTR_FRIENDLY_NAME] == "KBeacon 459F Voltage"
    assert voltage_sensor_attrs[ATTR_UNIT_OF_MEASUREMENT] == UnitOfElectricPotential.VOLT
    assert voltage_sensor_attrs[ATTR_STATE_CLASS] == "measurement"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_voltage_only_sensor(hass: HomeAssistant) -> None:
    """Test device broadcasting only voltage."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:A0",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_VOLTAGE_ONLY_SERVICE_INFO)
    await hass.async_block_till_done()

    assert len(hass.states.async_all("sensor")) == 0

    enable_entity(hass, "sensor.kbeacon_45a0_voltage")
    await reload_entry(hass, entry)
    inject_bluetooth_service_info(hass, KBEACON_VOLTAGE_ONLY_SERVICE_INFO)
    await hass.async_block_till_done()

    # Only voltage sensor should be created once enabled
    assert len(hass.states.async_all("sensor")) == 1

    voltage_sensor = hass.states.get("sensor.kbeacon_45a0_voltage")
    assert voltage_sensor is not None
    assert voltage_sensor.state == "3.0"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_negative_temperature_sensor(hass: HomeAssistant) -> None:
    """Test device broadcasting negative temperature."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:A1",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_NEGATIVE_TEMP_SERVICE_INFO)
    await hass.async_block_till_done()

    # Only temperature sensor should be created
    assert len(hass.states.async_all("sensor")) == 1

    temp_sensor = hass.states.get("sensor.kbeacon_45a1_temperature")
    assert temp_sensor is not None
    assert temp_sensor.state == "-10.0"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_sensor_update_on_new_advertisement(hass: HomeAssistant) -> None:
    """Test sensors update when new BLE advertisement is received."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:9F",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_SERVICE_INFO)
    await hass.async_block_till_done()

    temp_sensor = hass.states.get("sensor.kbeacon_459f_temperature")
    assert temp_sensor.state == "27.28"

    # Inject new advertisement with different temperature
    # Temperature 20C = 5120 raw = 0x1400
    from . import make_bluetooth_service_info
    updated_service_info = make_bluetooth_service_info(
        name="KBPro_142081",
        address="BC:57:29:02:45:9F",
        rssi=-60,
        service_data={"0000feaa-0000-1000-8000-00805f9b34fb": bytes.fromhex("2100021400")},
        manufacturer_data={},
        service_uuids=["0000feaa-0000-1000-8000-00805f9b34fb"],
        source="local",
    )

    inject_bluetooth_service_info(hass, updated_service_info)
    await hass.async_block_till_done()

    temp_sensor = hass.states.get("sensor.kbeacon_459f_temperature")
    assert temp_sensor.state == "20.0"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_lux_and_co2_sensors(hass: HomeAssistant) -> None:
    """Test device broadcasting FEAA light and CO2 fields."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:A2",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_LUX_CO2_SERVICE_INFO)
    await hass.async_block_till_done()

    # Temperature, humidity, light, and CO2 are enabled by default.
    assert len(hass.states.async_all("sensor")) == 4

    lux_sensor = hass.states.get("sensor.kbeacon_45a2_illuminance")
    assert lux_sensor is not None
    assert lux_sensor.state == "300"
    assert lux_sensor.attributes[ATTR_UNIT_OF_MEASUREMENT] == LIGHT_LUX

    co2_sensor = hass.states.get("sensor.kbeacon_45a2_carbon_dioxide")
    assert co2_sensor is not None
    assert co2_sensor.state == "1000"
    assert (
        co2_sensor.attributes[ATTR_UNIT_OF_MEASUREMENT]
        == CONCENTRATION_PARTS_PER_MILLION
    )

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_system_battery_sensor(hass: HomeAssistant) -> None:
    """Test device broadcasting FEAA system-frame battery field."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:A3",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_SYSTEM_BATTERY_SERVICE_INFO)
    await hass.async_block_till_done()

    battery_sensor = hass.states.get("sensor.kbeacon_45a3_battery")
    assert battery_sensor is not None
    assert battery_sensor.state == "97"
    assert battery_sensor.attributes[ATTR_UNIT_OF_MEASUREMENT] == PERCENTAGE

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()


async def test_uid_tx_power_sensor(hass: HomeAssistant) -> None:
    """Test device broadcasting FEAA UID Tx power field."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:A4",
    )
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    inject_bluetooth_service_info(hass, KBEACON_UID_TX_POWER_SERVICE_INFO)
    await hass.async_block_till_done()

    assert hass.states.get("sensor.kbeacon_45a4_uid_tx_power") is None

    enable_entity(hass, "sensor.kbeacon_45a4_uid_tx_power")
    await reload_entry(hass, entry)
    inject_bluetooth_service_info(hass, KBEACON_UID_TX_POWER_SERVICE_INFO)
    await hass.async_block_till_done()

    uid_tx_power_sensor = hass.states.get("sensor.kbeacon_45a4_uid_tx_power")
    assert uid_tx_power_sensor is not None
    assert uid_tx_power_sensor.state == "-12"
    assert uid_tx_power_sensor.attributes[ATTR_UNIT_OF_MEASUREMENT] == "dBm"

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
