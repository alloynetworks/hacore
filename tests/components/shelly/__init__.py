"""Tests for the Shelly integration."""
from copy import deepcopy
from typing import Any
from unittest.mock import Mock

import pytest

from homeassistant.components.shelly.const import CONF_SLEEP_PERIOD, DOMAIN
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry

MOCK_MAC = "123456789ABC"


async def init_integration(
    hass: HomeAssistant, gen: int, model="SHSW-25", sleep_period=0
) -> MockConfigEntry:
    """Set up the Shelly integration in Home Assistant."""
    data = {
        CONF_HOST: "192.168.1.37",
        CONF_SLEEP_PERIOD: sleep_period,
        "model": model,
        "gen": gen,
    }

    entry = MockConfigEntry(domain=DOMAIN, data=data, unique_id=MOCK_MAC)
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    return entry


def mutate_rpc_device_status(
    monkeypatch: pytest.MonkeyPatch,
    mock_rpc_device: Mock,
    top_level_key: str,
    key: str,
    value: Any,
) -> None:
    """Mutate status for rpc device."""
    new_status = deepcopy(mock_rpc_device.status)
    new_status[top_level_key][key] = value
    monkeypatch.setattr(mock_rpc_device, "status", new_status)
