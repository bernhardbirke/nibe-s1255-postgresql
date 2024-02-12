import pytest
import datetime
from src.nibe.data import NibeToPostgres
from src.nibe.config import Configuration
from src.nibe.postgresql_tasks import PostgresTasks
from src.nibe.exceptions import (
    WrongData,
    DataCollectionError,
    UnknownRegisterTypeError,
    NoConnectionError,
)


@pytest.fixture  # instance of Class NibeToPostgres
def nibetopostgres():
    # instance of Configuration class
    config = Configuration()
    # instance of PostgresTasks
    client = PostgresTasks()
    # initialize location
    return NibeToPostgres(
        config,
        client,
    )


@pytest.fixture  # data response as transmitted by Nibe Modbus TCP/IP
def responsedata_gradminuten():
    response = 62869
    return response


def test_process_value(nibetopostgres):
    assert nibetopostgres.process_value(62869, 10, "gradminuten", 0) == -266.7
    assert (
        nibetopostgres.process_value(29312, 10, "heizung_nur_verdichter", 4) == 29145.6
    )
    assert (
        nibetopostgres.process_value(245, 10, "aktuelle_vorlauftemperatur", 0) == 24.5
    )
