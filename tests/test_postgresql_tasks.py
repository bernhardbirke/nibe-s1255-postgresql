import pytest
from src.nibe.postgresql_tasks import PostgresTasks


# create instance postgrestasks of Class PostgresTasks
@pytest.fixture
def postgrestasks():
    return PostgresTasks()


# Caution: creates an entry in specified postgresql database
def test_insert_nibe(postgrestasks):
    id = postgrestasks.insert_nibe(
        -7.8,
        24.3,
        21.2,
        4.2,
        -2.0,
        43.0,
        37.2,
        20.1,
        24.7,
        8.0,
        -412,
        43,
        19283,
        1306932,
        432,
        8930,
        27891,
        9,
        1,
    )
    assert isinstance(id, int) and id > 0
