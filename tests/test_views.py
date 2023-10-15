from unittest.mock import patch
from weather_ab import views


# @patch('weather_ab.views.requests')
def test_weather_view_caching(client, settings, tmp_path):
    settings.CACHES['default']['LOCATION'] = tmp_path

    with patch('weather_ab.views.requests') as mrequests:
        mrequests.get.return_value.json.return_value = {
            'fact': {
                'temp': 99, 'wind_speed': 33, 'pressure_mm': 888
            }
        }

        resp = client.get('/weather?city=Иркутск')
        assert resp.status_code == 200
        mrequests.get.assert_called_once()

        resp = client.get('/weather?city=Иркутск')
        assert resp.status_code == 200
        assert mrequests.get.call_count == 1

    
