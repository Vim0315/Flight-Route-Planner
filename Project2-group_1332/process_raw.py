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
import pandas as pd


def process_raw() -> None:
    """Process, read and save the datasets."""
    # read datasets
    routes_raw = pd.read_csv("routes.csv")
    airports_raw = pd.read_csv("Airports.csv", error_bad_lines=False)

    # clean extra spaces
    routes_raw.columns = routes_raw.columns.to_series().apply(lambda x: x.strip())
    airports_raw.columns = airports_raw.columns.to_series().apply(lambda x: x.strip())

    # only select relevant columns for later analysis
    routes = routes_raw[['airline', 'source airport', 'destination apirport']]
    airports = airports_raw[['codeIataAirport', 'nameAirport',
                             'latitudeAirport', 'longitudeAirport',
                             'nameCountry', 'routes']]

    airports_1 = airports.rename(columns={'codeIataAirport': 'source airport',
                                          'nameAirport': 's_name',
                                          'latitudeAirport': 's_lat',
                                          'longitudeAirport': 's_long',
                                          'nameCountry': 's_country',
                                          'routes': 's_popularity'})

    merged_1 = pd.merge(routes, airports_1, on='source airport', how='left')

    airports_2 = airports.rename(columns={'codeIataAirport': 'destination apirport',
                                          'nameAirport': 'd_name',
                                          'latitudeAirport': 'd_lat',
                                          'longitudeAirport': 'd_long',
                                          'nameCountry': 'd_country',
                                          'routes': 'd_popularity'})

    processed_routes = pd.merge(merged_1,
                                airports_2,
                                on='destination apirport',
                                how='left')

    return processed_routes
