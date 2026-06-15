import heapq
from .common import bind_search_functions

def a_star(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, get_heuristic_fn = bind_search_functions(bat_dau, dich)
    
    h_start = get_heuristic_fn(node)
    if check_goal_fn(node):
        return [node], 1, "Tìm thấy", {
            "cost": 0,
            "values": [0],
            "values_g": [0],
            "values_h": [0],
            "values_f": [0],
            "history_h": [0]
        }
    
    counter = 0
    frontier = []
    heapq.heappush(frontier, (h_start, counter, node))
    
    parent = {node: None}
    node_g = {node: 0}
    node_h = {node: h_start}
    node_f = {node: h_start}
    best_g = {node: 0}
    so_node = 0
    
    while frontier:
        f, _, current_node = heapq.heappop(frontier)
        so_node += 1
        
        current_g = best_g.get(current_node, float('inf'))
        
        if check_goal_fn(current_node):
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            ds_g = [node_g[s] for s in path]
            ds_h = [node_h[s] for s in path]
            ds_f = [node_f[s] for s in path]
            return path, so_node, "Tìm thấy", {
                "cost": current_g,
                "values": ds_f,
                "values_g": ds_g,
                "values_h": ds_h,
                "values_f": ds_f,
                "history_h": ds_h
            }
            
        if current_g > best_g.get(current_node, float('inf')):
            continue
            
        for child in get_successors_fn(current_node):
            step_cost = 1
            g_child = current_g + step_cost
            h_child = get_heuristic_fn(child)
            f_child = g_child + h_child
            
            if child not in best_g or g_child < best_g[child]:
                best_g[child] = g_child
                parent[child] = current_node
                node_g[child] = g_child
                node_h[child] = h_child
                node_f[child] = f_child
                counter += 1
                heapq.heappush(frontier, (f_child, counter, child))
                 
    return None, so_node, "Không tìm thấy", {}
