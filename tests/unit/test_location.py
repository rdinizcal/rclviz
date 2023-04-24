import unittest
from unittest.mock import patch, Mock
from location import fetch_location, LocationNotFoundError

class TestLocation(unittest.TestCase):
    
    @patch('location.Nominatim')
    def test_fetch_location(self, mock_nominatim):
        mock_geolocator = mock_nominatim.return_value
        mock_location = Mock()
        mock_location.latitude = 40.7128
        mock_location.longitude = -74.0060
        mock_geolocator.geocode.return_value = mock_location
        
        location = fetch_location("New York University")
        
        self.assertEqual(location, {'lat': 40.7128, 'lng': -74.0060})
        mock_geolocator.geocode.assert_called_once_with("New York University")
        
    @patch('location.Nominatim')
    def test_fetch_location_not_found(self, mock_nominatim):
        mock_geolocator = mock_nominatim.return_value
        mock_geolocator.geocode.return_value = None
        
        with self.assertRaises(LocationNotFoundError):
            fetch_location("Nonexistent University")
            
        mock_geolocator.geocode.assert_called_once_with("Nonexistent University")

    def test_fetch_location_additional():
        # Test University of Pernambuco
        result = location.fetch_location("University of Pernambuco")
        assert result == {'lat': -8.0278246, 'lng': -34.9505235}

        # Test University of Singapore
        result = location.fetch_location("University of Singapore")
        assert result == {'lat': 1.2965886, 'lng': 103.7766665}

        # Test University of Madagascar
        with pytest.raises(location.LocationNotFoundError):
            location.fetch_location("University of Madagascar")
