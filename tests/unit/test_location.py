import pytest
from unittest.mock import patch, Mock
from rclviz.location import fetch_location, LocationNotFoundError

@pytest.fixture
def mock_nominatim():
    with patch('rclviz.location.Nominatim') as mock_nominatim:
        yield mock_nominatim

def test_fetch_location(mock_nominatim):
    mock_geolocator = mock_nominatim.return_value
    mock_location = Mock()
    mock_location.latitude = 40.7128
    mock_location.longitude = -74.0060
    mock_geolocator.geocode.return_value = mock_location

    location = fetch_location("New York University")

    assert location == {'lat': 40.7128, 'lng': -74.0060}
    mock_geolocator.geocode.assert_called_once_with("New York University")

def test_fetch_location_not_found(mock_nominatim):
    mock_geolocator = mock_nominatim.return_value
    mock_geolocator.geocode.return_value = None

    with pytest.raises(LocationNotFoundError):
        fetch_location("Nonexistent University")

    mock_geolocator.geocode.assert_called_once_with("Nonexistent University")

def test_fetch_location_additional():
    # Test University of Pernambuco
    result = fetch_location("University of Pernambuco")
    assert result == {'lat': -8.052423600000001, 'lng': -34.9510615050235}

    # Test University of Singapore
    result = fetch_location("University of Singapore")
    assert result == {'lat': 1.2962018, 'lng': 103.77689943784759}

    # Test University of Madagascar
    with pytest.raises(LocationNotFoundError):
        fetch_location("University of Madagascar")