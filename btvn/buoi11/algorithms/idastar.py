from .common import bind_search_functions

def ida_star(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, get_heuristic_fn = bind_search_functions(bat_dau, dich)
            
    h_start = get_heuristic_fn(node)
    if check_goal_fn(node):
        return [node], 1, f"Tìm thấy (threshold = {h_start})", {
            "cost": 0,
            "values": [0],
            "values_g": [0],
            "values_h": [0],
            "values_f": [0],
            "threshold": h_start,
            "threshold_history": [h_start],
            "history_h": [0]
        }
        
    threshold = h_start
    tong_node = 0
    threshold_history = []
    
    def search(current_node, g_hien_tai, duong, ds_g, ds_h, ds_f):
        nonlocal tong_node
        tong_node += 1
        
        h_val = get_heuristic_fn(current_node)
        f_val = g_hien_tai + h_val
        
        if f_val > threshold:
            return f_val, None
            
        if check_goal_fn(current_node):
            return "found", (duong, ds_g, ds_h, ds_f)
            
        min_over = float('inf')
        
        for child in get_successors_fn(current_node):
            if child not in duong:
                step_cost = 1
                g_child = g_hien_tai + step_cost
                h_child = get_heuristic_fn(child)
                f_child = g_child + h_child
                
                res, val = search(child, g_child, duong + [child], ds_g + [g_child], ds_h + [h_child], ds_f + [f_child])
                
                if res == "found":
                    return "found", val
                if res < min_over:
                    min_over = res
                    
        return min_over, None

    while True:
        threshold_history.append(threshold)
        res, val = search(node, 0, [node], [0], [h_start], [h_start])
        
        if res == "found":
            duong, ds_g, ds_h, ds_f = val
            return duong, tong_node, f"Tìm thấy (threshold = {threshold})", {
                "cost": ds_g[-1],
                "values": ds_f,
                "values_g": ds_g,
                "values_h": ds_h,
                "values_f": ds_f,
                "threshold": threshold,
                "threshold_history": threshold_history,
                "history_h": ds_h
            }
        if res == float('inf'):
            return None, tong_node, "Không tìm thấy", {}
        
        threshold = res
