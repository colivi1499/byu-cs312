import math
import random
from collections import deque
import copy
import heapq

from tsp_core import Tour, SolutionStats, Timer, score_tour, Solver
from tsp_cuttree import CutTree


def random_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    while True:
        if timer.time_out():
            break

        tour = random.sample(list(range(len(edges))), len(edges))
        n_nodes_expanded += 1

        cost = score_tour(tour, edges)
        if math.isinf(cost):
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        if stats and cost > stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    
    return stats


def greedy_tour(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    n_nodes_expanded = 0
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))

    for node in range(len(edges)):
        if timer.time_out():
            break

        tour, is_complete = create_greedy_tour(edges, node)
        n_nodes_expanded += 1

        if not is_complete:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        cost = score_tour(tour, edges)


        if stats and cost >= stats[-1].score:
            n_nodes_pruned += 1
            cut_tree.cut(tour)
            continue

        stats.append(SolutionStats(
            tour=tour,
            score=cost,
            time=timer.time(),
            max_queue_size=1,
            n_nodes_expanded=n_nodes_expanded,
            n_nodes_pruned=n_nodes_pruned,
            n_leaves_covered=cut_tree.n_leaves_cut(),
            fraction_leaves_covered=cut_tree.fraction_leaves_covered()
        ))

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            1,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    
    return stats


def dfs(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    stats = []
    max_queue_size = 1
    n_nodes_expanded = 1
    n_nodes_pruned = 0
    cut_tree = CutTree(len(edges))
    stack = deque()
    stack.append((0,[0],0)) # curr_node, tour, curr_cost


    while stack:
        if timer.time_out():
            break

        curr_node, tour, cost = stack.pop()

        if len(tour) == len(edges):
            if edges[curr_node][0] != math.inf:
                total_cost = cost + edges[curr_node][0]

                if stats and total_cost >= stats[-1].score:
                    n_nodes_pruned += 1
                    cut_tree.cut(tour)
                    continue

                stats.append(SolutionStats(
                    tour=tour,
                    score=total_cost,
                    time=timer.time(),
                    max_queue_size=max_queue_size,
                    n_nodes_expanded=n_nodes_expanded,
                    n_nodes_pruned=n_nodes_pruned,
                    n_leaves_covered=cut_tree.n_leaves_cut(),
                    fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                ))
            continue

        for neighbor in range(len(edges)):
            if neighbor not in tour and edges[curr_node][neighbor] != math.inf:
                stack.append((neighbor, tour + [neighbor], cost + edges[curr_node][neighbor]))
                n_nodes_expanded += 1
                if len(stack) > max_queue_size:
                    max_queue_size = len(stack)
            elif edges[curr_node][neighbor] == math.inf:
                n_nodes_pruned += 1
                cut_tree.cut(tour)


    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            max_queue_size,
            n_nodes_expanded,
            n_nodes_pruned,
            cut_tree.n_leaves_cut(),
            cut_tree.fraction_leaves_covered()
        )]
    return stats


def branch_and_bound(edges, timer):
    stats = []
    max_queue_size = 1
    n_nodes_expanded = 1
    cut_tree = CutTree(len(edges))
    n_nodes_pruned = 0
    best_score = math.inf
    best_tour = None
    initial_result = greedy_tour(edges,timer)[-1]

    priority_queue = []
    heapq.heappush(priority_queue, (0, [0], 0))

    while priority_queue:
        if timer.time_out():
            break

        lower_bound, tour, cost = heapq.heappop(priority_queue)

        if len(tour) == len(edges):
            if edges[tour[-1]][0] != math.inf:
                total_cost = cost + edges[tour[-1]][0]
                if total_cost < best_score:
                    best_score = total_cost
                    best_tour = tour

                    stats.append(SolutionStats(
                        tour=best_tour,
                        score=best_score,
                        time=timer.time(),
                        max_queue_size=max_queue_size,
                        n_nodes_expanded=n_nodes_expanded,
                        n_nodes_pruned=n_nodes_pruned,
                        n_leaves_covered=cut_tree.n_leaves_cut(),
                        fraction_leaves_covered=cut_tree.fraction_leaves_covered()
                    ))

            continue

        for neighbor in range(len(edges)):
            if neighbor not in tour and edges[tour[-1]][neighbor] != math.inf:
                new_tour = tour + [neighbor]
                new_cost = cost + edges[tour[-1]][neighbor]
                
                new_lower_bound = calculate_lower_bound(edges, new_tour)

                if new_lower_bound >= best_score:
                    n_nodes_pruned += 1
                    cut_tree.cut(tour)
                    continue

                heapq.heappush(priority_queue, (new_lower_bound, new_tour, new_cost))
                n_nodes_expanded += 1

                if len(priority_queue) > max_queue_size:
                    max_queue_size = len(priority_queue)

    if not stats:
        return [SolutionStats(
            [],
            math.inf,
            timer.time(),
            max_queue_size,
            n_nodes_expanded,
            n_nodes_pruned,
            0,
            0
        )]

    return stats


def branch_and_bound_smart(edges: list[list[float]], timer: Timer) -> list[SolutionStats]:
    return []



def create_greedy_tour(edges: list[list[float]], start: int) -> tuple[list[int], bool]:
    tour: list[int] = []
    visited: set[int] = set()
    curr_node = start
    visited.add(curr_node)
    tour.append(curr_node)
    n=0
    while len(visited) < len(edges):
        smallest: int = curr_node
        smallest_cost = math.inf
        n += 1
        neighbors_checked = 0
        for neighbor in range(len(edges)):
            if (neighbor not in visited) and (edges[curr_node][neighbor] < smallest_cost):
                smallest = neighbor
                smallest_cost = edges[curr_node][smallest]
                neighbors_checked += 1

        if smallest_cost == math.inf:
            return tour, False

        curr_node = smallest
        tour.append(curr_node)
        visited.add(curr_node)

    if (math.isinf(edges[curr_node][start])):
        return tour, False

    return tour, True

def reduce_cost_matrix(edges):
    n = len(edges)
    reduced_matrix = [row[:] for row in edges]

    for i in range(n):
        min_row = min(reduced_matrix[i])
        for j in range(n):
            reduced_matrix[i][j] -= min_row
    
    for j in range(n):
        min_col = min(reduced_matrix[i][j] for i in range(n))
        for i in range(n):
            reduced_matrix[i][j] -= min_col
    
    return reduced_matrix

def calculate_lower_bound(edges, tour):
    lower_bound = 0
    for i in range(len(tour) - 1):
        lower_bound += edges[tour[i]][tour[i+1]]
    
    for i in range(len(edges)):
        if i not in tour:
            min_edge = min(edges[i][j] for j in range(len(edges)) if j != i)
            lower_bound += min_edge
    
    return lower_bound
