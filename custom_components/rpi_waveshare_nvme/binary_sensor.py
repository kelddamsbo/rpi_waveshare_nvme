"""Binary sensor entities."""

# region #-- imports --#
from dataclasses import dataclass
from typing import Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import NVME, NVMEEntity
from .const import CONF_COORDINATOR, CONF_MIN_CHARGING, DEF_MIN_CHARGING, DOMAIN

# endregion


@dataclass
class NVMEBinarySensorDescriptionMixin:
    """Additional attributes of the binary sensor description."""

    value_fn: Callable[[NVME], bool]


@dataclass
class NVMEBinarySensorEntityDescription(
    BinarySensorEntityDescription, UPSBinarySensorDescriptionMixin
):
    """Describes NVME binary sensor entity."""


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create the binary sensor entities."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][CONF_COORDINATOR]

    binary_sensors: list[NVMEBinarySensorEntity] = [
        NVMEBinarySensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMEBinarySensorEntityDescription(
                device_class=BinarySensorDeviceClass.BATTERY_CHARGING,
                key="battery_state",
                name="Battery State",
                translation_key="battery_state",
                value_fn=lambda u: u.current
                >= config_entry.options.get(CONF_MIN_CHARGING, DEF_MIN_CHARGING),
            ),
        ),
    ]

    async_add_entities(binary_sensors, update_before_add=True)


class NVMEBinarySensorEntity(NVMEEntity, BinarySensorEntity):
    """Representation of a NVME binary sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: NVMEBinarySensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialise."""
        super().__init__(config_entry=config_entry, coordinator=coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_unique_id = (
            f"{config_entry.entry_id}::binary_sensor::{self.entity_description.key}"
        )

    @property
    def is_on(self) -> bool:
        """Return binary sensor state."""
        return self.entity_description.value_fn(self.coordinator.data)
