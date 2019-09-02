import collections
from itertools import combinations

def form_dict_graph(res):
    '''
    :param res: [(business_1, business_2), (business_1, business_2), ...]
    :return: {root: [child_1, child_2, ...], root: [child_1, child_2, ...]}
    '''
    graph = {}
    for comb in res:
        try:
            graph[comb[0]].append(comb[1])
        except:
            graph[comb[0]] = [comb[1]]
        try:
            graph[comb[1]].append(comb[0])
        except:
            graph[comb[1]] = [comb[0]]
    return graph


def compute_betweeness(graph):
    '''
    :param graph: {root: [child_1, child_2, ...], root: [child_1, child_2, ...]}
    :return: {(node_1, node_2): float, (node_1, node_2): float, ...}
    '''
    all_edges = {}
    for key in graph.keys():
        level = 1
        levels = {level: [key]}
        queue = collections.deque([key])
        temp = {}
        visited = set()
        while queue:
            next_queue = collections.deque([])
            while queue:
                h = queue.popleft()
                visited.add(h)
                temp[h] = temp.get(h, 0) + 1
                for child in graph[h]:
                    if child not in visited and child not in queue:
                        next_queue.append(child)
            level += 1
            queue = next_queue
            if next_queue:
                levels[level] = list(set(next_queue))
        res = {key: 1 for key in temp.keys()}
        for level in sorted(levels.keys())[::-1][:-1]:
            current_level = levels[level]
            for current_node in current_level:
                all_connected_nodes = graph[current_node]
                for all_connected_node in all_connected_nodes:
                    if all_connected_node in levels[level - 1]:
                        pair = tuple(set([all_connected_node, current_node]))
                        res[all_connected_node] += float(res[current_node]) / temp[current_node]
                        all_edges[pair] = all_edges.get(pair, 0) + float(res[current_node]) / temp[current_node]
    return all_edges


def partition(graph):
    '''
    :param graph:  {root: [child_1, child_2, ...], root: [child_1, child_2, ...]}
    :return: [[], [], ...]
    '''
    all_node = list(graph.keys())

    partition = []

    while all_node:
        start = all_node[0]
        # keep track of all visited nodes
        explored = []
        # keep track of nodes to be checked
        queue = [start]

        visited = [start]  # to avoid inserting the same node twice into the queue

        # keep looping until there are nodes still to be checked
        while queue:
            # pop shallowest node (first node) from queue
            node = queue.pop(0)
            explored.append(node)
            all_node.pop(all_node.index(node))
            neighbours = graph[node]

            # add neighbours of node to queue
            for neighbour in neighbours:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.append(neighbour)
        partition.append(explored)

    return partition

def modulatiry(partitions, graph, new_graph, m):
    '''
    :param partitions: [[], [], ...]
    :param graph: {root: [child_1, child_2, ...], root: [child_1, child_2, ...]}
    :param new_graph: {root: [child_1, child_2, ...], root: [child_1, child_2, ...]}
    :param m: int
    :return: [modularity_1, modularity_2, ...]
    '''
    res = []
    for partition in partitions:
        temp = 0
        for comb in combinations(partition, 2):
            A = 1 if comb[1] in graph[comb[0]] else 0
            k_i = len(new_graph[comb[0]])
            k_j = len(new_graph[comb[1]])
            temp += A - (k_i * k_j) / float(m)
        res.append(temp)
    return res

