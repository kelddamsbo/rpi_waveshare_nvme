"""Sensor entities."""

# region #-- imports --#
from dataclasses import dataclass
from typing import Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import NVME, NVMEEntity
from .const import CONF_COORDINATOR, DOMAIN

# endregion


@dataclass
class NVMESensorEntityDescription(SensorEntityDescription):
    """Describes NVME sensor entity."""

    value_fn: Callable[[NVME], StateType] | None = None


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Create the sensor entities."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][CONF_COORDINATOR]

    sensors: list[NVMESensorEntity] = [
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.BATTERY,
                key="battery_percentage",
                name="Battery Level",
                native_unit_of_measurement=PERCENTAGE,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="battery_percentage",
            ),
        ),
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.CURRENT,
                key="current",
                name="Current",
                native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="current",
            ),
        ),
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.VOLTAGE,
                key="load_voltage",
                name="Load Voltage",
                native_unit_of_measurement=UnitOfElectricPotential.VOLT,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="load_voltage",
            ),
        ),
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.POWER,
                key="power",
                name="Power",
                native_unit_of_measurement=UnitOfPower.WATT,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="power",
            ),
        ),
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.VOLTAGE,
                key="",
                name="PSU Voltage",
                native_unit_of_measurement=UnitOfElectricPotential.VOLT,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="psu_voltage",
                value_fn=lambda u: u.load_voltage + u.shunt_voltage,
            ),
        ),
        NVMESensorEntity(
            config_entry=config_entry,
            coordinator=coordinator,
            description=NVMESensorEntityDescription(
                device_class=SensorDeviceClass.VOLTAGE,
                key="shunt_voltage",
                name="Shunt Voltage",
                native_unit_of_measurement=UnitOfElectricPotential.VOLT,
                state_class=SensorStateClass.MEASUREMENT,
                translation_key="shunt_voltage",
            ),
        ),
    ]

    async_add_entities(sensors, update_before_add=True)


class NVMESensorEntity(NVMEEntity, SensorEntity):
    """Representation of a NVME sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        description: NVMESensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialise."""
        super().__init__(config_entry=config_entry, coordinator=coordinator)
        self.entity_description = description
        self._attr_has_entity_name = True
        self._attr_unique_id = (
            f"{config_entry.entry_id}::sensor::{self.entity_description.key}"
        )

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        if isinstance(self.entity_description.value_fn, Callable):
            return self.entity_description.value_fn(self.coordinator.data)

        return getattr(self.coordinator.data, self.entity_description.key, None)
