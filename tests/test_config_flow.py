"""Test the KBeacon BLE config flow."""

from unittest.mock import patch

import pytest

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kbeacon.const import DOMAIN

from . import KBEACON_SERVICE_INFO, NOT_KBEACON_SERVICE_INFO


@pytest.fixture(autouse=True)
def expected_lingering_timers() -> bool:
    """Allow known bluetooth manager timer during config flow tests."""
    return True


async def test_async_step_bluetooth_valid_device(hass: HomeAssistant) -> None:
    """Test discovery via bluetooth with a valid device."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"
    with patch(
        "custom_components.kbeacon.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "KBeacon 459F"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "BC:57:29:02:45:9F"


async def test_async_step_bluetooth_not_kbeacon(hass: HomeAssistant) -> None:
    """Test discovery via bluetooth not kbeacon."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=NOT_KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "not_supported"


async def test_async_step_user_no_devices_found(hass: HomeAssistant) -> None:
    """Test setup from service info cache with no devices found."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_USER},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_user_with_found_devices(hass: HomeAssistant) -> None:
    """Test setup from service info cache with devices found."""
    with patch(
        "custom_components.kbeacon.config_flow.async_discovered_service_info",
        return_value=[KBEACON_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    with patch(
        "custom_components.kbeacon.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "BC:57:29:02:45:9F"},
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "KBeacon 459F"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "BC:57:29:02:45:9F"


async def test_async_step_user_device_added_between_steps(hass: HomeAssistant) -> None:
    """Test the device gets added via another flow between steps."""
    with patch(
        "custom_components.kbeacon.config_flow.async_discovered_service_info",
        return_value=[KBEACON_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:9F",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.kbeacon.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "BC:57:29:02:45:9F"},
        )
    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "already_configured"


async def test_async_step_user_with_found_devices_already_setup(
    hass: HomeAssistant,
) -> None:
    """Test setup from service info cache with devices found."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:9F",
    )
    entry.add_to_hass(hass)

    with patch(
        "custom_components.kbeacon.config_flow.async_discovered_service_info",
        return_value=[KBEACON_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_bluetooth_devices_already_setup(hass: HomeAssistant) -> None:
    """Test we can't start a flow if there is already a config entry."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="BC:57:29:02:45:9F",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_async_step_bluetooth_already_in_progress(hass: HomeAssistant) -> None:
    """Test we can't start a flow for the same device twice."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_in_progress"


async def test_async_step_user_takes_precedence_over_discovery(
    hass: HomeAssistant,
) -> None:
    """Test manual setup takes precedence over discovery."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": config_entries.SOURCE_BLUETOOTH},
        data=KBEACON_SERVICE_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    with patch(
        "custom_components.kbeacon.config_flow.async_discovered_service_info",
        return_value=[KBEACON_SERVICE_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_USER},
        )
        assert result["type"] is FlowResultType.FORM

    with patch(
        "custom_components.kbeacon.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={"address": "BC:57:29:02:45:9F"},
        )
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "KBeacon 459F"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "BC:57:29:02:45:9F"

    # Verify the original flow was canceled
    assert not hass.config_entries.flow.async_progress(DOMAIN)
