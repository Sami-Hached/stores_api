from unittest.mock import Mock

import pytest

from src.infrastructure.database import get_session


mock = Mock()

@pytest.fixture
def test_client():
    config = {
        "HOST": "localhost",
        "PASSWORD": "non_secret",
        "USER": "test-user",
        "DB": "learning_sql_test",
        "PORT": 5433,
    }
    with mock.patch("infrastructure.database.get_session") as mocked_session:
        session = get_session(config)
        mocked_session.return_value = session
    return session
