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
from build_graph import *
from graph import *
import visualization
from random import randint, choice


class FlightSimulation:
    """The simulation class for testing purposes."""
    _system: System
    _places: list
    type: str
    start: str
    end: str

    def __init__(self, num_destination: int, type: str):
        """The init method for flight simulation"""
        self._system = build_system()
        self._places = []
        self.type = type
        self._generate_random_destinations(num_destination)

    def _generate_random_destinations(self, num_destination: int) -> None:
        """Generate random destinations for the upcoming calls to algorithms"""
        entry_list = list(self._system.terminals.items())
        random.shuffle(entry_list)
        for i in range(num_destination):
            if i == 0:
                self.start = entry_list[i][1].name
            elif i == num_destination - 1:
                self.end = entry_list[i][1].name
            self._places.append(entry_list[i][1].name)

    def run_tsp(self) -> None:
        """Call the tsp algorithm and visualize the result"""
        tour = self._system.tsp(self._places[0], self._places[1:], self._places[0], self.type)
        visualization.tsp_visualization(self._system, tour, self.type)

    def run_dp_tsp(self) -> None:
        """Call the dynamic programming approach of tsp and visualize the result"""
        tour = self._system.dp_tsp(self._places[0], self._places[1:], self.type)
        if tour[1] == []:
            tour = self._system.tsp(self._places[0], self._places[1:], self._places[0], self.type)
        visualization.tsp_visualization(self._system, tour, self.type)

    def run_dfs(self) -> None:
        """Call dfs algotirhm and visualize the result"""
        state = self._system.dfs(self.start, self.end, self.type)
        if state is False or state.moves == []:
            pass
        else:
            visualization.one_to_one_visualization(self._system, state, self.type)

    def run_bfs(self) -> None:
        """Call bfs algotirhm and visualize the result"""
        state = self._system.bfs(self.start, self.end, self.type)
        if state is False or state.moves == []:
            pass
        else:
            visualization.one_to_one_visualization(self._system, state, self.type)

    def run_a_star_search(self) -> None:
        """Call A* search algotirhm and visualize the result"""
        state = self._system.bfs(self.start, self.end, self.type)
        if state is False or state.moves == []:
            pass
        else:
            visualization.one_to_one_visualization(self._system, state, self.type)

    def run_a_star_search_augmented(self) -> None:
        """Call the augumented A* search algotirhm and visualize the result"""
        state = self._system.a_star_search_augmented(self._places[:len(self._places) // 2],
                                                     self._places[len(self._places) // 2:],
                                                     self.type)
        if state and state.moves != []:
            visualization.one_to_one_visualization(self._system, state, self.type)


def run_simulation() -> None:
    """Run a random simulation"""
    simulation = FlightSimulation(randint(3, 6), choice(['distance', 'price']))
    simulation.run_bfs()
    simulation.run_dfs()
    simulation.run_tsp()
    simulation.run_dp_tsp()
    simulation.run_a_star_search()
    simulation.run_a_star_search_augmented()
