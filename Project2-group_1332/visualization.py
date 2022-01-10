"""CSC111 Final Project 2021

Copyright and Usage Information =============================== This file is part of the CSC111
final project: Ready for Departure!, developed by Charlie Guo, Owen Zhang, Terry Tu,
Vim Du. This file is provided solely for the course evaluation purposes of CSC111 at University
of Toronto St. George campus. All forms of distribution of this code, whether as given or with
any changes, are strictly prohibited. The code may have referred to sources beyond the course
materials, which are all cited properly in project report. For more information on copyright for
this project, please contact any of the group members.

This file is Copyright (c) 2021 Charlie Guo, Owen Zhang, Terry Tu and Vim Du.
"""
from graph import *
from build_graph import *
from main import *
import plotly.offline as py
import plotly.graph_objs as go
import plotly.io as pio
from graph import *
from process_raw import *
pio.renderers.default = "browser"


def one_to_one_visualization(system, state, heurestic) -> None:
    """plot the one-to-one search result on the map"""
    moves = state.moves
    routes = system.get_routes_info(moves, heurestic)
    terminals = []
    for route in routes:
        terminals.append(route.dep)
    terminals.append(routes[-1].arr)
    terminals = [system.terminals[terminal] for terminal in terminals]
    term_lat = [terminal.lat for terminal in terminals]
    term_long = [terminal.long for terminal in terminals]
    term_names = [terminal.name for terminal in terminals]
    term_codes = [terminal.code for terminal in terminals]

    airportspy = [dict(
        type='scattergeo',
        locationmode='country names',
        lon=term_long,
        lat=term_lat,
        text=['<b>' + 'Airport Name:' + term_codes[i] + '</b>' \
              + '<br>' + 'Airport Code: ' + term_names[i]
              for i in range(len(term_names))],
        hoverinfo='text',
        marker=dict(
            size=3,
            sizemin=2,
            color="black",
            cmin=10.565915336317195,
            cmax=38.383341806128094,
            colorscale=[[0, 'rgb(255, 255, 0)'], [1, 'rgb(255, 0, 0)']],
            colorbar=go.scattergeo.marker.ColorBar(
                title='Score'
            ),
            opacity=1,
            line=dict(
                width=0,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

    flight_paths = []
    for i in range(len(terminals) - 1):
        aux_origin = terminals[i]
        aux_destin = terminals[i + 1]

        flight_paths.append(
            dict(
                type='scattergeo',
                locationmode='country names',
                lon=[float(aux_origin.long), float(aux_destin.long)],
                lat=[float(aux_origin.lat), float(aux_destin.lat)],
                mode='lines',
                hoverinfo='skip',
                line=dict(
                    width=0.5,
                )
            )
        )
        # opacity=float(flights.loc[i, 'COUNT'] / maxcount_f) * 2

    layout = go.Layout(
        showlegend=False,
        geo=dict(
            scope='world',
            projection=dict(type='orthographic', scale=1.8),
            showland=True,
            showocean=True,
            showcoastlines=True,
            showcountries=True,
            landcolor='rgb(49, 49, 49)',
            countrycolor='rgb(90, 90, 90)',
            coastlinecolor='rgb(90, 90, 90)',
            oceancolor='rgb(29, 29, 29)',
            bgcolor='rgb(29, 29, 29)',
            center=dict(lon=term_long[len(term_long) // 2], lat=term_lat[len(term_lat) // 2])
        ),
        title=dict(
            text=get_paths(routes),
            font=dict(family='Sherif',
                      size=20,
                      color='orange'),
            y=0.9, x=0.5,
            xanchor='center',
            yanchor='top'),
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        autosize=True,
        paper_bgcolor='rgb(29, 29, 29)',
        plot_bgcolor='rgb(29, 29, 29)'
    )

    fig = dict(data=flight_paths + airportspy, layout=layout)
    # py.offline.iplot(fig, filename='routes-graph')
    py.plot(fig, filename='routes-graph', auto_open=True)


def tsp_visualization(system, tour, heurestic) -> None:
    """plot the tsp routes on the map"""
    if isinstance(tour, tuple):
        routes = system.get_routes_info(tour[1], heurestic)
    else:
        routes = system.get_routes_info(tour.moves, heurestic)

    # Stores all Terminal objects
    terminals = []
    for route in routes:
        terminals.append(route.dep)
    terminals.append(routes[0].dep)
    terminals = [system.terminals[terminal] for terminal in terminals]
    term_lat = [terminal.lat for terminal in terminals]
    term_long = [terminal.long for terminal in terminals]
    term_names = [terminal.name for terminal in terminals]
    term_codes = [terminal.code for terminal in terminals]

    airportspy = [dict(
        type='scattergeo',
        locationmode='country names',
        lon=term_long,
        lat=term_lat,
        text=['<b>' + 'Airport Name:' + term_codes[i] + '</b>' \
              + '<br>' + 'Airport Code: ' + term_names[i]
              for i in range(len(term_names))],
        hoverinfo='text',
        marker=dict(
            size=3,
            sizemin=2,
            color="black",
            cmin=10.565915336317195,
            cmax=38.383341806128094,
            colorscale=[[0, 'rgb(255, 255, 0)'], [1, 'rgb(255, 0, 0)']],
            colorbar=go.scattergeo.marker.ColorBar(
                title='Score'
            ),
            opacity=1,
            line=dict(
                width=0,
                color='rgba(68, 68, 68, 0)'
            )
        ))]

    flight_paths = []
    for i in range(len(terminals) - 1):
        aux_origin = terminals[i]
        aux_destin = terminals[i + 1]

        flight_paths.append(
            dict(
                type='scattergeo',
                locationmode='country names',
                lon=[float(aux_origin.long), float(aux_destin.long)],
                lat=[float(aux_origin.lat), float(aux_destin.lat)],
                mode='lines',
                hoverinfo='skip',
                line=dict(
                    width=0.5,
                )
            )
        )

    layout = go.Layout(
        showlegend=False,
        geo=dict(
            scope='world',
            projection=dict(type='orthographic', scale=1.8),
            showland=True,
            showocean=True,
            showcoastlines=True,
            showcountries=True,
            landcolor='rgb(49, 49, 49)',
            countrycolor='rgb(90, 90, 90)',
            coastlinecolor='rgb(90, 90, 90)',
            oceancolor='rgb(29, 29, 29)',
            bgcolor='rgb(29, 29, 29)',
            center=dict(lon=term_long[len(term_long) // 2], lat=term_lat[len(term_lat) // 2])
        ),
        title=dict(
            text=get_paths(routes),
            font=dict(family='Sherif',
                      size=18,
                      color='orange'),
            y=0.9, x=0.5,
            xanchor='center',
            yanchor='top'),
        margin=go.layout.Margin(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        autosize=True,
        paper_bgcolor='rgb(29, 29, 29)',
        plot_bgcolor='rgb(29, 29, 29)'
    )

    fig = dict(data=flight_paths + airportspy, layout=layout)
    # py.offline.iplot(fig, filename='routes-graph')
    py.plot(fig, filename='routes-graph.html', auto_open=True)


def get_paths(routes) -> str:
    """Retrieve the path text from the given routes, so that we can display the
    information."""
    total_cost = 0
    total_distance = 0
    paths = ""
    paths += routes[0].dep
    for route in routes:
        paths += " --> " + route.arr
        total_cost += route.price
        total_distance += route.distance
    for i in range(len(paths)):
        if i == 123:
            paths = paths[:i] + '<br>' + paths[i:]
    return "Optimized path:" + paths + '' + '<br>' + 'Total Cost: ' + \
           '$' + str((total_cost / 5).__round__(2)) \
           + ' <br> Total Distance: ' + str(total_distance.__round__(2)) + 'km'
