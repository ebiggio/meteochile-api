import plotly.graph_objects as go
import json


def create_regional_map():
    """
    Draws a map of Chile with the regions as the polygons

    The ID of each polygon is the region code (1-16) to be used as a location, obtained from the geojson file
    :return: A plotly figure object
    """
    with open('chile_regions.geojson') as json_file:
        chile_regions = json.load(json_file)

    fig = go.Figure(data=go.Choropleth(
        geojson=chile_regions,
        featureidkey="properties.codregion",
        )
    )

    fig.update_geos(fitbounds="locations", visible=False)

    return fig
