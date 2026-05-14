import pytest

URL_BASE = "https://petstore.swagger.io/v2"


@pytest.fixture
def base_url():
    return URL_BASE
