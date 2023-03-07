import requests as requests
import plotly.graph_objects as go
import chile_maps


def get_main_station_daily_weather():
    # Get the day's weather data from 21 main stations
    return _process_get_request('https://climatologia.meteochile.gob.cl/application/productos/boletinClimatologicoDiario')


def get_all_stations_metadata():
    # Get metadata from all 119 stations
    return _process_get_request('https://climatologia.meteochile.gob.cl/application/productos/estacionesRedEma')


def _process_get_request(endpoint):
    try:
        api_request = requests.get(endpoint)
    except requests.exceptions.RequestException as e:
        return False

    if api_request.status_code == requests.codes.ok:
        return api_request.json()
    else:
        return dict()


# Step 1: Get all stations metadata
# Step 2: Get weather data from 21 main stations
# Step 3: Merge data from step 1 and 2 for the 21 main stations
# Step 4: Plot maximum and minimum temperatures from 21 main stations for the current day as a choropleth map
# Step 5: Display geolocation of 21 main stations in the map

# TODO
# - Plot historical data for a given station (ideally, using a selector for the station and a date picker/slider for the date)


if __name__ == '__main__':
    all_station_data = get_all_stations_metadata()
    main_station_data = get_main_station_daily_weather()

    station_coordinates_lats = []
    station_coordinates_longs = []
    station_names = []
    region_codes = []

    maximum_temperature = []
    minimum_temperature = []

    for main_station in main_station_data:
        for station_data in all_station_data['datosEstacion']:
            if station_data['codigoNacional'] == main_station['metaDatos']['estacion']['codigoNacional']:
                main_station['metaDatos']['latitud'] = station_data['latitud']
                main_station['metaDatos']['longitud'] = station_data['longitud']

                station_coordinates_lats.append(station_data['latitud'])
                station_coordinates_longs.append(station_data['longitud'])
                station_names.append(str(station_data['region']) + ' - ' + station_data['nombreEstacion'])
                region_codes.append(station_data['region'])

                maximum_temperature.append(main_station['datos']['temperaturaMaxima'])
                minimum_temperature.append(main_station['datos']['temperaturaMinima'])
                break

    plotly_fig = chile_maps.create_regional_map()

    plotly_fig.update_traces(
        locations=region_codes,  # Spatial coordinates
        z=maximum_temperature,  # Data to be color-coded
        colorscale="Reds",
        colorbar_title="Temperature (°C)",
    )

    plotly_fig.add_trace(
        go.Scattergeo(
            lon=station_coordinates_longs,
            lat=station_coordinates_lats,
            mode="markers",
            marker=dict(
                color='LightSkyBlue',
                size=8,
                line=dict(
                    color='MediumPurple',
                    width=2
                )
            ),
            text=station_names,
        )
    )

    plotly_fig.update_layout(
        title_text='Maximum temperatures',
        geo_scope='south america',
    )

    plotly_fig.show()
