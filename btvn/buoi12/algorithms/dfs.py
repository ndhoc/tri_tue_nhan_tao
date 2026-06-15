from .common import bind_search_functions

def dfs(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, _ = bind_search_functions(bat_dau, dich)
            
    if check_goal_fn(node): 
        return [node], 1, "Tìm thấy", {"cost": 0, "values": [0]}

    frontier = [node]
    parent = {node: None}
    so_node = 0

    while frontier:
        curr = frontier.pop()
        so_node += 1
        if check_goal_fn(curr): 
            path = []
            temp = curr
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            return path, so_node, "Tìm thấy", {"cost": len(path) - 1, "values": list(range(len(path)))}
        
        for child in get_successors_fn(curr):
            if child not in parent:
                parent[child] = curr
                if check_goal_fn(child):
                    path = []
                    temp = child
                    while temp is not None:
                        path.append(temp)
                        temp = parent[temp]
                    path.reverse()
                    return path, so_node, "Tìm thấy", {"cost": len(path) - 1, "values": list(range(len(path)))}
                frontier.append(child)
    return None, so_node, "Không tìm thấy", {}
