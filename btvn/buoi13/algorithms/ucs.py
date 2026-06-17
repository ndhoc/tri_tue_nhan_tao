import heapq
from .common import bind_search_functions

def ucs(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, _ = bind_search_functions(bat_dau, dich)

    if check_goal_fn(node): 
        return [node], 1, "Tìm thấy", {"cost": 0, "values": [0]}

    counter = 0
    frontier = []
    heapq.heappush(frontier, (0, counter, node))
    
    parent = {node: None}
    node_cost = {node: 0}
    node_depth = {node: 0}
    best_cost = {node: 0}
    so_node = 0

    while frontier:
        cost, _, current_node = heapq.heappop(frontier)
        so_node += 1

        if check_goal_fn(current_node): 
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            ds_cost = [node_cost[s] for s in path]
            return path, so_node, "Tìm thấy", {"cost": cost, "values": ds_cost}

        ds_con = get_successors_fn(current_node)
        so_con_parent = len(ds_con)
        
        for child in ds_con:
            depth_child = node_depth[current_node] + 1
            step_cost = depth_child + so_con_parent
            new_cost = cost + step_cost

            if child not in best_cost or new_cost < best_cost[child]:
                best_cost[child] = new_cost
                parent[child] = current_node
                node_cost[child] = new_cost
                node_depth[child] = depth_child
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, child))

    return None, so_node, "Không tìm thấy", {}
