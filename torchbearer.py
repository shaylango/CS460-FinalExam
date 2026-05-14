"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Shayla Ngo
Student ID:   828275819

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    return(
        "- A single shortest-path run from S is not enough because it'll only find the min distance to each node, "
        "but not the best order for visiting multiple relics.\n"
        "- The decision that remains after all inter-location costs are known is the best order for visiting all the relics.\n"
        "- This requires a search over orders because there are different costs depending on the order of relics."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    sources = set([spawn] + relics)
    return list(sources)


def run_dijkstra(graph, source):
    distances = {node: float('inf') for node in graph}
    distances[source] = 0
    priority_queue = [(0, source)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.get(current_node, []):

            if current_distance + weight < distances[neighbor]:
                distances[neighbor] = current_distance + weight
                heapq.heappush(priority_queue, (distances[neighbor], neighbor))

    return distances


def precompute_distances(graph, spawn, relics, exit_node):
    distance_table = {}
    sources = select_sources(spawn, relics, exit_node)

    for source in sources:
        distance_table[source] = run_dijkstra(graph, source)
    
    return distance_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    return (
        "- The stored distance is the optimal shortest path from the source.\n"
        "- The distance is the shortest path that is known so far, which only uses the finalized nodes along the path.\n"
        "- The distance of the source is 0 and all the others are infinity, which there are no wrong distances at the start.\n"
        "- Having nonnegative edge weights means that no shorter path could be found through an unvisited node.\n"
        "- All nodes that are finalized have the optimal shortest path from the source.\n"
        "- Correct distances make sure that the route planner chooses the min cost path."
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    return(
        "- Greedy picks the closest next relic without considering the cost of the route.\n"
        "- Starting at S, B cost 1, while C and D cost 2, which moving between relics could have different costs.\n"
        "- Greedy picks B first because it is the closest relic.\n"
        "- S -> B -> D -> C -> T, total cost of 4\n"
        "- Choosing the closest next relic does not always result in having a lower total cost.\n"
        "- The algorithm must explore every possible order in which the relics can be visited to find the min total cost."
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    best = [float('inf'), []]
    current_loc = spawn
    relics_remaining = set(relics)
    relics_visited_order = []
    cost_so_far = 0

    _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best)
    
    return best[0], best[1]


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    #It is safe to prune because if we were to do any more exploration, then the cost would only increase, which can't beat the current best cost.
    if cost_so_far >= best[0]:
        return
    
    if not relics_remaining:
        dist_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total_cost = cost_so_far + dist_to_exit

        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = relics_visited_order.copy()
        return
    
    for next_relic in relics_remaining:
        travel_cost = dist_table.get(current_loc, {}).get(next_relic, float('inf'))

        if travel_cost != float('inf'):
            relics_remaining.remove(next_relic)
            relics_visited_order.append(next_relic)

            _explore(dist_table, next_relic, relics_remaining, relics_visited_order,
                     cost_so_far + travel_cost, exit_node, best)
            
            relics_visited_order.pop()
            relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
