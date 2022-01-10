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
from typing import Any, Union
import math
import random


class Terminal:
    """The class for a terminal."""

    def __init__(self, name, code, country, long, lat, popularity) -> None:
        """The init method for a terminal"""
        self.name = name
        self.code = code
        self.country = country
        self.long = long
        self.lat = lat
        self.popularity = popularity


class Route:
    """The class for a flight route."""

    def __init__(self, dep, arr, airlines, distance, flight_number, ticket_price) -> None:
        """The init method for a flight route."""
        self.dep = dep
        self.arr = arr
        self.airlines = airlines
        self.distance = distance
        self.flight = flight_number
        self.price = ticket_price


class PQueue:
    """The class for a PQueue."""

    def __init__(self) -> None:
        """The init method for a PQueue."""
        self.c = {}

    def push(self, x, v) -> None:
        """The push method for a PQueue."""
        if v not in self.c:
            self.c[v] = []
        self.c[v].append(x)

    def extract_min(self) -> Terminal:
        """The method of extracting the smallest terminal for a PQueue."""
        min_key = min(self.c.keys())
        terminal = self.c[min_key][0]

        self.c[min_key].pop(0)
        if self.c[min_key] == []:
            self.c.pop(min_key)
        return terminal

    def is_not_empty(self) -> bool:
        """Check if the PQueue is empty."""

        return self.c != {}


class State:
    """The State object including the route information"""

    def __init__(self, pos) -> None:
        """The init method for State."""
        self.terminal = pos
        self.moves = [pos]
        self.total_distance = 0


class System:
    """The System object, the main core of our project"""

    def __init__(self) -> None:
        """The init method for system"""
        self.terminals = {}
        self.routes = {}

    def add_terminal(self, name, code, country, long, lat, pop) -> None:
        """Add a terminal to the system."""
        if name not in self.terminals:
            self.terminals[name] = Terminal(name, code, country, long, lat, pop)

    def add_route(self, t1, t2, airline, dist, flight, price) -> None:
        """Add a route to the system."""
        if t1 in self.terminals and t2 in self.terminals:
            dep, arr = t1, t2
            route = Route(dep, arr, airline, dist, flight, price)
            if (dep, arr) not in self.routes:
                self.routes[(dep, arr)] = []
            self.routes[(dep, arr)].append(route)
        else:
            raise ValueError

    def has_flight(self, t1: Any, t2: Any) -> bool:
        """check if the flight exists."""
        if t1 in self.terminals and t2 in self.terminals:
            return (t1, t2) in self.routes
        return False

    def get_distance(self, v1, v2, type) -> float:
        """get the distance between two terminals."""
        inf = float('inf')
        if type == "distance":
            R = 6373.0
            t1, t2 = self.terminals[v1], self.terminals[v2]

            lat1, lon1 = math.radians(t1.lat), math.radians(t1.long)
            lat2, lon2 = math.radians(t2.lat), math.radians(t2.long)

            dlon = lon2 - lon1
            dlat = lat2 - lat1

            # Haversine formula
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c

            return distance

        elif type == "price":
            return min([route.price for route in self.routes[(v1, v2)]]) if (v1,
                                                                             v2) in self.routes else inf

    def generate_price(self, v1, v2) -> float:
        """Generate the price for the flight tickets."""
        t1, t2 = self.terminals[v1], self.terminals[v2]
        same_country = 1 if t1.country == t2.country else 1.05
        distance = self.get_distance(v1, v2, "distance")
        if distance != 0:
            standard = math.log(150, distance * 0.6) * distance * 1.1
            random_factor = random.uniform(0.85, 1.15)
            return standard * same_country * random_factor

    def find_next_state(self, state, type) -> list[State]:
        """Find the next state"""
        if state.terminal in self.terminals:
            res = []
            for v1, v2 in self.routes.keys():
                if v1 == state.terminal:
                    new_state = State(v2)
                    new_state.moves = state.moves[:]
                    new_state.total_distance = state.total_distance + self.get_distance(v1, v2,
                                                                                        type)
                    new_state.moves.append(v2)
                    res.append(new_state)
            return res

    def heuristic(self, t, goal, type="dist") -> Union[float, int]:
        """return the heuristic of the algorithms"""
        if type == "dist":
            return self.get_distance(t, goal, "distance") * 4
        elif type == "price":
            return self.get_distance(t, goal, "price") * 4
        elif type == "time":
            return 0

    def dfs(self, start: str, target: str, type: str) -> Union[State, bool]:
        """The dfs algorithm."""
        stack = list()
        stack.append(State(start))
        seen = [start]
        while stack:
            cur_state = stack.pop(-1)
            if cur_state.terminal == target:
                return cur_state
            for s in self.find_next_state(cur_state, type):
                if s.terminal not in seen:
                    stack.append(s)
                    seen.append(s.terminal)
        return False

    def bfs(self, start: str, target: str, type: str) -> Union[State, bool]:
        """The bfs algorithm."""
        queue = list()
        queue.append(State(start))
        seen = [start]
        while queue:
            cur_state = queue.pop(0)
            if cur_state.terminal == target:
                return cur_state
            for s in self.find_next_state(cur_state, type):
                if s.terminal not in seen:
                    queue.append(s)
                    seen.append(s.terminal)
        return False

    def a_star_search(self, start: str, target: str, type) -> Union[State, bool]:
        """The A* algorithm."""
        queue = PQueue()
        queue.push(State(start), self.heuristic(start, target))
        seen = [start]
        while queue.is_not_empty():
            cur_state = queue.extract_min()
            if cur_state.terminal == target:
                return cur_state
            for s in self.find_next_state(cur_state, type):
                f = self.heuristic(s.terminal, target)
                if s.terminal not in seen:
                    queue.push(s, f)
                    seen.append(s.terminal)
        return False

    def a_star_search_augmented(self, start_cities: list[str], destination_cities: list[str],
                                type: str) -> State:
        """ Based on the previously constructed astar search algorithm, augment it so that it
        allows user to have multiple departure and destination cities and outputs a State that
        has the least cost between some city pairs.
        """
        min_cost = float("inf")
        min_state = None
        for start in start_cities:
            for dest in destination_cities:
                cur_state = self.a_star_search(start, dest, type)
                if cur_state and cur_state.total_distance < min_cost:
                    min_cost = cur_state.total_distance
                    min_state = cur_state
        return min_state

    # World Tour Planning
    def tsp(self, start: str, stops, end: str, type: str) -> State:
        """Find the best route that start from a point,
        passes all the stops and ends at a point.
        In the returned tuple, the first item is the distance and the second is the cost"""
        if stops == []:  # when there is no stops
            return self.a_star_search(start, end, type)
        else:
            distances = []
            states = []
            for i in range(len(stops)):
                current_stop = stops[i]
                copy = stops.copy()
                copy.pop(i)
                cur_state = self.a_star_search(start, current_stop, type)
                rest_state = self.tsp(current_stop, copy, end, type)

                tot_distance = \
                    cur_state.total_distance + rest_state.total_distance
                # extent the cur_state
                cur_state.moves.extend(rest_state.moves[1:])
                cur_state.total_distance += rest_state.total_distance
                distances.append(tot_distance)
                states.append(cur_state)
            minimum_index = distances.index(min(distances))
            return states[minimum_index]

    def dp_tsp(self, start: str, stops, type: str) -> tuple:
        """The dynamic approach of tsp algorithm"""
        num_pos = len(stops) + 1
        stops.insert(0, start)
        inf = float('inf')
        min_dist = [[inf for _ in range(num_pos)] for _ in range(1 << num_pos)]

        min_path = [[[] for _ in range(num_pos)] for _ in range(1 << num_pos)]

        for s in range(1, 2 ** num_pos, 2):
            # ignore all stops row where "start" is not included since we want to travel back to
            # start at the end
            if not (s & 1):
                continue
            for j in range(1, num_pos):
                # Consider starting from j, and want to explore all the vertices once in S.
                if not (s & (1 << j)):
                    # if j is not in s, then we don't bother exploring because in this case,
                    # j is not suppose to be explored according to S
                    continue
                if s == int((1 << j) | 1):
                    # If in S there's only j and start two vertices left, then it's simply j ->
                    # start because we want it to end at start
                    min_path[s][j] = [j]
                    min_dist[s][j] = min(
                        self.get_distance(start, stops[j], type) if self.has_flight(start, stops[
                            j]) else inf, inf)

                for i in range(1, num_pos):
                    # consider the rest vertices that's not in s
                    if s & (1 << i):
                        # i is either j or start which we've already discussed or
                        # i -> j -> exploring {s} will cause i to be explored twice.
                        continue

                    if min_dist[s][j] + min(self.get_distance(stops[j], stops[i], type), inf) < \
                            min_dist[s | (1 << i)][
                                i]:
                        # if we find a new vertex i -> j -> {s} that has less distance for us to
                        # explore {s+i}, via the path of i->j->{s}, we update a new min distance
                        # for "starting from i, explore all {s+i} and end up at start".
                        min_path[s | (1 << i)][i] = min_path[s][j] + [i]
                        min_dist[s | (1 << i)][i] = min_dist[s][j] + min(
                            self.get_distance(stops[j], stops[i], type) if self.has_flight(stops[j],
                                                                                           stops[
                                                                                               i]) else inf,
                            inf)

        ans_dist = inf
        ans_path = []

        for i in range(1, num_pos):
            if min_dist[2 ** num_pos - 1][i] + min(
                    self.get_distance(stops[i], start, type) if self.has_flight(stops[i],
                                                                                start) else inf,
                    inf) < ans_dist:
                # the last line of min_path represents the min distance starting from i,
                # exploring all of the vertices and end up at start. since we begin with start,
                # we add up the distance from start to those vertices, with the min-distance they
                # can have to explore the all the remaining vertices to get an overall minimum
                # distance to "start from start, end at start, explore all vertices path".
                ans_path = [start] + [stops[p] for p in min_path[2 ** num_pos - 1][i]] + [start]
                ans_dist = min_dist[(1 << num_pos) - 1][i] + min(
                    self.get_distance(stops[i], start, type) if self.has_flight(start,
                                                                                stops[i]) else inf,
                    inf)

        return ans_dist, ans_path

    def get_routes_info(self, path: list[str], type: str) -> list[Route]:
        """Get the route information for the path."""
        paths = []
        for i in range(len(path) - 1):
            min_num = float("inf")
            min_route = None
            if type == "distance":
                for route in self.routes[(path[i], path[i + 1])]:
                    if route.distance < min_num:
                        min_num = route.distance
                        min_route = route
            elif type == "price":
                for route in self.routes[(path[i], path[i + 1])]:
                    if route.price < min_num:
                        min_num = route.price
                        min_route = route
            paths.append(min_route)
        return paths
