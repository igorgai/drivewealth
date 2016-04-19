import pytest


def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="",
        help="Username for DriveWealth API")
    parser.addoption("--password", action="store", default="",
        help="Password for DriveWealth API")


@pytest.fixture
def username(request):
    return request.config.getoption("--username")


@pytest.fixture
def password(request):
    return request.config.getoption("--password")
