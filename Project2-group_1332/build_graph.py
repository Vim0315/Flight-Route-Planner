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
from process_raw import *

# initialize column index names
AIRLINE = 0
S_CODE = 1
D_CODE = 2

S_NAME = 3
S_LAT = 4
S_LONG = 5
S_COUNTRY = 6
S_POP = 7

D_NAME = 8
D_LAT = 9
D_LONG = 10
D_COUNTRY = 11
D_POP = 12


def build_system() -> System:
    """Build up the computing system."""
    routes = process_raw().values.tolist()
    system = System()
    num = 0
    for route in routes:
        system.add_terminal(route[S_CODE], route[S_NAME], route[S_COUNTRY],
                            float(".".join(str(route[S_LONG]).split(","))),
                            float(".".join(str(route[S_LAT]).split(","))),
                            float(route[S_POP]))
        system.add_terminal(route[D_CODE], route[D_NAME], route[D_COUNTRY],
                            float(".".join(str(route[D_LONG]).split(","))),
                            float(".".join(str(route[D_LAT]).split(","))),
                            float(route[D_POP]))
        distance = system.get_distance(route[S_CODE], route[D_CODE], "distance")
        if distance != 0:
            price = system.generate_price(route[S_CODE], route[D_CODE])
            flight_num = route[AIRLINE] + str(10000 + num)
            system.add_route(route[S_CODE], route[D_CODE], route[AIRLINE], distance, flight_num, price)
            num += 1
    return system
