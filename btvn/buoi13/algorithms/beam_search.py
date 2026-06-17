import random
from .common import bind_search_functions

def local_beam_search(bat_dau, dich, k=5, max_steps=1000):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, get_heuristic_fn = bind_search_functions(bat_dau, dich)
            
    current_states = [(node, [node])]
    visited_states = {node}
    
    attempts = 0
    while len(current_states) < k and attempts < 200:
        attempts += 1
        curr = node
        path = [node]
        steps = random.randint(1, 6)
        for _ in range(steps):
            children = get_successors_fn(curr)
            if children:
                curr = random.choice(children)
                if curr not in path:
                    path.append(curr)
        if curr not in visited_states:
            visited_states.add(curr)
            current_states.append((curr, path))
            
    if len(current_states) < k:
        for child in get_successors_fn(node):
            if child not in visited_states:
                visited_states.add(child)
                current_states.append((child, [node, child]))
                if len(current_states) == k:
                    break
                    
    so_node = len(current_states)
    
    for state, path in current_states:
        if check_goal_fn(state):
            ds_cost = [get_heuristic_fn(s) for s in path]
            return path, so_node, "Tìm thấy (trong tập khởi tạo)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
    step_count = 0
    while step_count < max_steps:
        step_count += 1
        neighbor_states = []
        
        for state, path in current_states:
            for child in get_successors_fn(state):
                if child not in path:
                    neighbor_states.append((child, path + [child]))
                    
        if not neighbor_states:
            current_states.sort(key=lambda x: get_heuristic_fn(x[0]))
            best_state, best_path = current_states[0]
            ds_cost = [get_heuristic_fn(s) for s in best_path]
            return best_path, so_node, "Bế tắc (Thất bại)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
        so_node += len(neighbor_states)
        
        for child, path in neighbor_states:
            if check_goal_fn(child):
                ds_cost = [get_heuristic_fn(s) for s in path]
                return path, so_node, "Tìm thấy", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
                
        neighbor_states.sort(key=lambda x: get_heuristic_fn(x[0]))
        current_states = neighbor_states[:k]
        
    current_states.sort(key=lambda x: get_heuristic_fn(x[0]))
    best_state, best_path = current_states[0]
    ds_cost = [get_heuristic_fn(s) for s in best_path]
    return best_path, so_node, f"Thất bại (vượt quá {max_steps} bước)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
