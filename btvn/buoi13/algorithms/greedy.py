import heapq
from .common import bind_search_functions

def greedy_search(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, get_heuristic_fn = bind_search_functions(bat_dau, dich)
            
    h_start = get_heuristic_fn(node)
    if check_goal_fn(node): 
        return [node], 1, "Tìm thấy", {"heuristic": h_start, "values": [h_start], "history_h": [h_start]}

    counter = 0
    frontier = []
    heapq.heappush(frontier, (h_start, counter, node))
    
    parent = {node: None}
    node_h = {node: h_start}
    reached = {node}
    so_node = 0

    while frontier:
        h, _, current_node = heapq.heappop(frontier)
        so_node += 1

        if check_goal_fn(current_node): 
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            ds_h = [node_h[s] for s in path]
            return path, so_node, "Tìm thấy", {"heuristic": 0, "values": ds_h, "history_h": ds_h, "h_start": h_start}

        for child in get_successors_fn(current_node):
            if child not in reached:
                reached.add(child)
                parent[child] = current_node
                h_child = get_heuristic_fn(child)
                node_h[child] = h_child
                counter += 1
                heapq.heappush(frontier, (h_child, counter, child))

    return None, so_node, "Không tìm thấy", {}
