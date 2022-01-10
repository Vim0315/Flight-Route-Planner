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
import timeit
import random

if __name__ == "__main__":
    def print_paths(routes) -> None:
        """Print the paths for the testing purposes"""
        total_cost = 0
        total_distance = 0
        paths = ""
        for route in routes:
            paths += route.dep + "-->" + route.arr + "     "
            total_cost += route.price
            total_distance += route.distance

        print("Path: ", paths)
        print("Total cost $", total_cost // 5)
        print("Total Distance(km):", total_distance)


    # World Tour
    system = build_system()

    counter = 0
    terminals = [terminal for terminal in system.terminals if
                 system.terminals[terminal].popularity > 30]
    random.shuffle(terminals)
    p2p_terminals = terminals[:2]
    tsp_terminals = terminals[:21]

    print("=============== DP-TSP TESTING ===============")
    for i in range(3, 5):
        start_time = timeit.default_timer()
        term = tsp_terminals[:i]
        tour = system.dp_tsp(tsp_terminals[i], term, "price")
        print("Running Time with {} terminals is: {}s ".format(i,
                                                               timeit.default_timer() - start_time))
        print_paths(system.get_routes_info(tour[1], "price"))
        print()

    # DFS O(|V| + |E|)
    print("=============== DFS TESTING ===============")
    start_time = timeit.default_timer()
    for a in p2p_terminals:
        for b in p2p_terminals:
            if a != b:
                system.dfs(a, b, "price")
    print("Running Time: ", timeit.default_timer() - start_time)
    # BFS O(|V| + |E|)
    print("=============== BFS TESTING ===============")
    start_time = timeit.default_timer()
    for a in p2p_terminals:
        for b in p2p_terminals:
            if a != b:
                system.bfs(a, b, "price")
    print("Running Time: ", timeit.default_timer() - start_time)
    # Astar O(|V| + |E|)
    print("=============== A* TESTING ===============")
    start_time = timeit.default_timer()
    for a in p2p_terminals:
        for b in p2p_terminals:
            if a != b:
                system.a_star_search(a, b, "price")
    print("Running Time: ", timeit.default_timer() - start_time)

    # Astar-TSP O(n^n), where n is the total number of terminals
    print("=============== AStar-TSP TESTING ===============")
    for i in range(3, 6):
        start_time = timeit.default_timer()
        term = tsp_terminals[:i]
        tour = system.tsp(tsp_terminals[i], term, tsp_terminals[i], "price")
        print("Running Time with {} terminals is: {}s ".format(i,
                                                               timeit.default_timer() - start_time))
        print_paths(system.get_routes_info(tour.moves, "price"))
        print()
    # DP-TSP O(n^2*2^n)
    print("=============== DP-TSP TESTING ===============")
    for i in range(5, 21, 5):
        start_time = timeit.default_timer()
        term = tsp_terminals[:i]
        tour = system.dp_tsp(tsp_terminals[i], term, "price")
        print("Running Time with {} terminals is: {}s ".format(i,
                                                               timeit.default_timer() - start_time))
        print_paths(system.get_routes_info(tour[1], "price"))
        print()
