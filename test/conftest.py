"""Pytest fixtures."""

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

import pytest
from picnic.data_vault import FieldDataType
from picnic.data_vault.field import Field
from picnic.data_vault.data_vault_load import DataVaultLoad
from picnic.data_vault.driving_key_field import DrivingKeyField
from picnic.data_vault.effectivity_satellite import EffectivitySatellite
from picnic.data_vault.hub import Hub
from picnic.data_vault.link import Link
from picnic.data_vault.role_playing_hub import RolePlayingHub
from picnic.data_vault.satellite import Satellite


# Pytest fixtures that depend on other fixtures defined in the same scope will
# trigger Pylint (Redefined name from outer scope). While usually valid, this doesn't
# make much sense in this case.
# pylint: disable=redefined-outer-name


@pytest.fixture
def extract_start_timestamp() -> datetime:
    """Define extraction start timestamp.

    Returns:
        Extraction start timestamp used for testing.
    """
    timestamp = datetime(2019, 8, 6, tzinfo=timezone.utc)
    return timestamp


@pytest.fixture
def test_path() -> Path:
    """Define test path.

    Returns:
        Parent directory of this file.
    """
    return Path(__file__).resolve().parent


@pytest.fixture
def process_configuration() -> Dict[str, str]:
    """Define process configuration.

    Returns:
        Process configuration.
    """
    config = {
        "source": "test",
        "extract_schema": "dv_extract",
        "extract_table": "extract_orders",
        "staging_schema": "dv_stg",
        "staging_table": "orders",
        "target_schema": "dv",
    }
    return config


@pytest.fixture
def h_customer(
    process_configuration: Dict[str, str], extract_start_timestamp: datetime
) -> Hub:
    """Define h_customer test hub.

    Args:
        process_configuration: Process configuration fixture value.
        extract_start_timestamp: Timestamp fixture value.

    Returns:
        Deserialized hub h_customer.
    """
    h_customer_fields = [
        Field(
            parent_table_name="h_customer",
            name="h_customer_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="h_customer",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=2,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_customer",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_customer",
            name="customer_id",
            data_type=FieldDataType.TEXT,
            position=4,
            is_mandatory=True,
        ),
    ]

    h_customer = Hub(
        schema=process_configuration["target_schema"],
        name="h_customer",
        fields=h_customer_fields,
    )
    h_customer.staging_schema = "dv_stg"
    h_customer.staging_table = (
        f"orders_{extract_start_timestamp.strftime('%Y%m%d_%H%M%S')}"
    )
    return h_customer


@pytest.fixture
def h_customer_test_role_playing(
    process_configuration: Dict[str, str],
    h_customer: Hub,
    extract_start_timestamp: datetime,
) -> RolePlayingHub:
    """Define h_customer_test_role_playing test hub.

    Args:
        process_configuration: Process configuration fixture value.
        h_customer: Hub customer fixture value.
        extract_start_timestamp: Timestamp fixture value.

    Returns:
        Deserialized role playing hub h_customer_test_role_playing.
    """
    h_customer_test_role_playing_fields = [
        Field(
            parent_table_name="h_customer_test_role_playing",
            name="h_customer_test_role_playing_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="h_customer_test_role_playing",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=2,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_customer_test_role_playing",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_customer_test_role_playing",
            name="customer_test_role_playing_id",
            data_type=FieldDataType.TEXT,
            position=4,
            is_mandatory=True,
        ),
    ]

    h_customer_test_role_playing = RolePlayingHub(
        schema=process_configuration["target_schema"],
        name="h_customer_test_role_playing",
        fields=h_customer_test_role_playing_fields,
    )
    h_customer_test_role_playing.parent_table = h_customer
    h_customer_test_role_playing.staging_schema = "dv_stg"
    h_customer_test_role_playing.staging_table = (
        f"orders_{extract_start_timestamp.strftime('%Y%m%d_%H%M%S')}"
    )

    return h_customer_test_role_playing


@pytest.fixture
def h_order(process_configuration: Dict[str, str]) -> Hub:
    """Define h_order test hub.

    Args:
        process_configuration: Process configuration fixture value.

    Returns:
        Deserialized hub h_order.
    """
    h_order_fields = [
        Field(
            parent_table_name="h_order",
            name="h_order_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="h_order",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=2,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_order",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="h_order",
            name="order_id",
            data_type=FieldDataType.TEXT,
            position=4,
            is_mandatory=True,
        ),
    ]
    h_order = Hub(
        schema=process_configuration["target_schema"],
        name="h_order",
        fields=h_order_fields,
    )
    return h_order


@pytest.fixture
def l_order_customer(
    process_configuration: Dict[str, str], extract_start_timestamp: datetime
) -> Link:
    """Define l_order_customer test link.

    Args:
        process_configuration: Process configuration fixture value.
        extract_start_timestamp: Timestamp fixture value.

    Returns:
        Deserialized link l_order_customer.
    """
    l_order_customer_fields = [
        Field(
            parent_table_name="l_order_customer",
            name="l_order_customer_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="h_order_hashkey",
            data_type=FieldDataType.TEXT,
            position=2,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="h_customer_hashkey",
            data_type=FieldDataType.TEXT,
            position=3,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="order_id",
            data_type=FieldDataType.TEXT,
            position=4,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="customer_id",
            data_type=FieldDataType.TEXT,
            position=5,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="ck_test_string",
            data_type=FieldDataType.TEXT,
            position=6,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="ck_test_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=7,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=8,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=9,
            is_mandatory=True,
        ),
    ]
    l_order_customer = Link(
        schema=process_configuration["target_schema"],
        name="l_order_customer",
        fields=l_order_customer_fields,
    )
    l_order_customer.staging_schema = "dv_stg"
    l_order_customer.staging_table = (
        f"orders_{extract_start_timestamp.strftime('%Y%m%d_%H%M%S')}"
    )

    return l_order_customer


@pytest.fixture
def l_order_customer_test_role_playing(process_configuration: Dict[str, str]) -> Link:
    """Define l_order_customer_test_role_playing test link.

    Args:
        process_configuration: Process configuration fixture value.

    Returns:
        Deserialized link l_order_customer_test_role_playing.
    """
    l_order_customer_test_role_playing_fields = [
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="l_order_customer_test_role_playing_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="h_order_hashkey",
            data_type=FieldDataType.TEXT,
            position=2,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="h_customer_test_role_playing_hashkey",
            data_type=FieldDataType.TEXT,
            position=3,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="order_id",
            data_type=FieldDataType.TEXT,
            position=4,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="customer_test_role_playing_id",
            data_type=FieldDataType.TEXT,
            position=5,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="ck_test_string",
            data_type=FieldDataType.TEXT,
            position=6,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="ck_test_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=7,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=8,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="l_order_customer_test_role_playing",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=9,
            is_mandatory=True,
        ),
    ]
    l_order_customer_test_role_playing = Link(
        schema=process_configuration["target_schema"],
        name="l_order_customer_test_role_playing",
        fields=l_order_customer_test_role_playing_fields,
    )
    return l_order_customer_test_role_playing


@pytest.fixture
def hs_customer(
    process_configuration: Dict[str, str], extract_start_timestamp: datetime
) -> Satellite:
    """Define hs_customer test satellite.

    Args:
        process_configuration: Process configuration fixture value.
        extract_start_timestamp: Timestamp fixture value.

    Returns:
        Deserialized satellite hs_customer.
    """
    hs_customer_fields = [
        Field(
            parent_table_name="hs_customer",
            name="h_customer_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="hs_customer",
            name="s_hashdiff",
            data_type=FieldDataType.TEXT,
            position=2,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="hs_customer",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="hs_customer",
            name="r_timestamp_end",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=4,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="hs_customer",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=5,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="hs_customer",
            name="test_string",
            data_type=FieldDataType.TEXT,
            position=6,
            is_mandatory=False,
        ),
        Field(
            parent_table_name="hs_customer",
            name="test_date",
            data_type=FieldDataType.DATE,
            position=7,
            is_mandatory=False,
        ),
        Field(
            parent_table_name="hs_customer",
            name="test_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=8,
            is_mandatory=False,
        ),
        Field(
            parent_table_name="hs_customer",
            name="test_integer",
            data_type=FieldDataType.NUMBER,
            position=9,
            is_mandatory=False,
            precision=38,
            scale=0,
        ),
        Field(
            parent_table_name="hs_customer",
            name="test_decimal",
            data_type=FieldDataType.NUMBER,
            position=10,
            is_mandatory=False,
            precision=18,
            scale=8,
        ),
        Field(
            parent_table_name="hs_customer",
            name="x_customer_id",
            data_type=FieldDataType.TEXT,
            position=11,
            is_mandatory=False,
        ),
        Field(
            parent_table_name="hs_customer",
            name="grouping_key",
            data_type=FieldDataType.TEXT,
            position=12,
            is_mandatory=False,
        ),
    ]
    hs_customer = Satellite(
        schema=process_configuration["target_schema"],
        name="hs_customer",
        fields=hs_customer_fields,
    )
    hs_customer.staging_schema = "dv_stg"
    hs_customer.staging_table = (
        f"orders_{extract_start_timestamp.strftime('%Y%m%d_%H%M%S')}"
    )

    return hs_customer


@pytest.fixture
def ls_order_customer_eff(
    process_configuration: Dict[str, str]
) -> EffectivitySatellite:
    """Define ls_order_customer_eff test (effectivity) satellite.

    Args:
        process_configuration: Process configuration fixture value.

    Returns:
        Deserialized effectivity satellite ls_order_customer_eff.
    """
    ls_order_customer_eff_fields = [
        Field(
            parent_table_name="ls_order_customer_eff",
            name="l_order_customer_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="ls_order_customer_eff",
            name="s_hashdiff",
            data_type=FieldDataType.TEXT,
            position=2,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="ls_order_customer_eff",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_eff",
            name="r_timestamp_end",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=4,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_eff",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=5,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_eff",
            name="dummy_descriptive_field",
            data_type=FieldDataType.TEXT,
            position=6,
            is_mandatory=True,
        ),
    ]

    driving_keys = [
        DrivingKeyField(
            name="h_customer_hashkey",
            parent_table_name="l_order_customer",
            satellite_name="ls_order_customer_eff",
        )
    ]

    ls_order_customer_eff = EffectivitySatellite(
        schema=process_configuration["target_schema"],
        name="ls_order_customer_eff",
        fields=ls_order_customer_eff_fields,
        driving_keys=driving_keys,
    )
    return ls_order_customer_eff


@pytest.fixture
def ls_order_customer_test_role_playing_eff(
    process_configuration: Dict[str, str]
) -> EffectivitySatellite:
    """Define ls_order_customer_test_role_playing_eff test (effectivity) satellite.

    Args:
        process_configuration: Process configuration fixture value.

    Returns:
        Deserialized effectivity satellite ls_order_customer_test_role_playing_eff.
    """
    ls_order_customer_test_role_playing_eff_fields = [
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="l_order_customer_test_role_playing_hashkey",
            data_type=FieldDataType.TEXT,
            position=1,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="s_hashdiff",
            data_type=FieldDataType.TEXT,
            position=2,
            is_mandatory=True,
            length=32,
        ),
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="r_timestamp",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=3,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="r_timestamp_end",
            data_type=FieldDataType.TIMESTAMP_NTZ,
            position=4,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="r_source",
            data_type=FieldDataType.TEXT,
            position=5,
            is_mandatory=True,
        ),
        Field(
            parent_table_name="ls_order_customer_test_role_playing_eff",
            name="dummy_descriptive_field",
            data_type=FieldDataType.TEXT,
            position=6,
            is_mandatory=True,
        ),
    ]

    driving_keys = [
        DrivingKeyField(
            name="h_customer_test_role_playing_hashkey",
            parent_table_name="l_order_customer_test_role_playing",
            satellite_name="ls_order_customer_test_role_playing_eff",
        )
    ]

    ls_order_customer_test_role_playing_eff = EffectivitySatellite(
        schema=process_configuration["target_schema"],
        name="ls_order_customer_test_role_playing_eff",
        fields=ls_order_customer_test_role_playing_eff_fields,
        driving_keys=driving_keys,
    )
    return ls_order_customer_test_role_playing_eff


@pytest.fixture
def data_vault_load(
    process_configuration: Dict[str, str],
    extract_start_timestamp: datetime,
    h_customer: Hub,
    h_order: Hub,
    l_order_customer: Link,
    hs_customer: Satellite,
    ls_order_customer_eff: EffectivitySatellite,
) -> DataVaultLoad:
    """Define an instance of DataVaultLoad that includes all test tables.

    Args:
        process_configuration: Process configuration fixture value.
        extract_start_timestamp: Extraction start timestamp fixture value.
        h_customer: Deserialized hub h_customer.
        h_order: Deserialized hub h_order.
        l_order_customer: Deserialized link l_order_customer.
        hs_customer: Deserialized satellite hs_customer.
        ls_order_customer_eff: Deserialized effectivity satellite ls_order_customer_eff.

    Returns:
        Instance of DataVaultLoad suitable for testing.
    """
    target_tables = [
        h_customer,
        h_order,
        l_order_customer,
        hs_customer,
        ls_order_customer_eff,
    ]
    data_vault_load_configuration = {
        "extract_schema": process_configuration["extract_schema"],
        "extract_table": process_configuration["extract_table"],
        "staging_schema": process_configuration["staging_schema"],
        "staging_table": process_configuration["staging_table"],
        "target_tables": target_tables,
        "source": process_configuration["source"],
    }
    return DataVaultLoad(
        **data_vault_load_configuration, extract_start_timestamp=extract_start_timestamp
    )


@pytest.fixture
def data_vault_load_with_role_playing(
    process_configuration: Dict[str, str],
    extract_start_timestamp: datetime,
    h_customer_test_role_playing: Hub,
    h_order: Hub,
    l_order_customer_test_role_playing: Link,
    ls_order_customer_test_role_playing_eff: EffectivitySatellite,
) -> DataVaultLoad:
    """Define an instance of DataVaultLoad for a model with a role playing hub.

    Args:
        process_configuration: Process configuration fixture value.
        extract_start_timestamp: Extraction start timestamp fixture value.
        h_customer_test_role_playing: Deserialized hub h_customer.
        h_order: Deserialized hub h_order.
        l_order_customer_test_role_playing: Deserialized link l_order_customer.
        ls_order_customer_test_role_playing_eff: Deserialized effectivity satellite
            ls_order_customer_eff.

    Returns:
        Instance of DataVaultLoad with role playing hub.
    """
    target_tables = [
        h_customer_test_role_playing,
        h_order,
        l_order_customer_test_role_playing,
        ls_order_customer_test_role_playing_eff,
    ]
    data_vault_load_configuration = {
        "extract_schema": process_configuration["extract_schema"],
        "extract_table": process_configuration["extract_table"],
        "staging_schema": process_configuration["staging_schema"],
        "staging_table": process_configuration["staging_table"],
        "target_tables": target_tables,
        "source": process_configuration["source"],
    }
    return DataVaultLoad(
        **data_vault_load_configuration, extract_start_timestamp=extract_start_timestamp
    )
