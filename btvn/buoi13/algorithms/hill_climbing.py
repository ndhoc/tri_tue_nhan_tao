import random
from .common import chuan_hoa_bat_dau, chuan_hoa_dich, la_trang_thai_belief, apply_action, tao_con, manhattan_distance, dem_o_sai_khong_tinh_0

def local_search(bat_dau, dich):
    node = chuan_hoa_bat_dau(bat_dau)
    dich_list = chuan_hoa_dich(dich)
    is_belief = la_trang_thai_belief(node)

    if is_belief:
        def check_goal_fn(st):
            for g in dich_list:
                if all(s == g for s in st):
                    return True
            return False
        def get_successors_fn(st):
            successors = []
            for action in ["U", "D", "L", "R"]:
                next_belief = tuple(apply_action(s, action) for s in st)
                successors.append(next_belief)
            return successors
        def get_misplaced_tiles_cost_fn(st):
            min_dist = float('inf')
            for g in dich_list:
                dist = sum(dem_o_sai_khong_tinh_0(s, g) for s in st)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
    else:
        dich_tuple = dich_list[0]
        def check_goal_fn(st):
            return st == dich_tuple
        def get_successors_fn(st):
            return tao_con(st)
        def get_misplaced_tiles_cost_fn(st):
            return dem_o_sai_khong_tinh_0(st, dich_tuple)
            
    current = node
    duong = [current]
    c_start = get_misplaced_tiles_cost_fn(current)
    ds_cost = [c_start]
    so_node = 0
    
    while True:
        so_node += 1
        if check_goal_fn(current):
            return duong, so_node, "Tìm thấy", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
        neighbors = get_successors_fn(current)
        current_cost = get_misplaced_tiles_cost_fn(current)
        
        found_better = False
        for neighbor in neighbors:
            neighbor_cost = get_misplaced_tiles_cost_fn(neighbor)
            if neighbor_cost < current_cost:
                current = neighbor
                duong.append(current)
                ds_cost.append(neighbor_cost)
                found_better = True
                break
                
        if not found_better:
            return duong, so_node, "Không tìm được nước đi (Thất bại)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}

def simple_hill_climbing(bat_dau, dich):
    node = chuan_hoa_bat_dau(bat_dau)
    dich_list = chuan_hoa_dich(dich)
    is_belief = la_trang_thai_belief(node)

    if is_belief:
        def check_goal_fn(st):
            for g in dich_list:
                if all(s == g for s in st):
                    return True
            return False
        def get_successors_fn(st):
            successors = []
            for action in ["U", "D", "L", "R"]:
                next_belief = tuple(apply_action(s, action) for s in st)
                successors.append(next_belief)
            return successors
        def get_misplaced_tiles_cost_fn(st):
            min_dist = float('inf')
            for g in dich_list:
                dist = sum(dem_o_sai_khong_tinh_0(s, g) for s in st)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
    else:
        dich_tuple = dich_list[0]
        def check_goal_fn(st):
            return st == dich_tuple
        def get_successors_fn(st):
            return tao_con(st)
        def get_misplaced_tiles_cost_fn(st):
            return dem_o_sai_khong_tinh_0(st, dich_tuple)
            
    current = node
    duong = [current]
    c_start = get_misplaced_tiles_cost_fn(current)
    ds_cost = [c_start]
    so_node = 0
    
    while True:
        so_node += 1
        if check_goal_fn(current):
            return duong, so_node, "Tìm thấy", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
        neighbors = get_successors_fn(current)
        current_cost = get_misplaced_tiles_cost_fn(current)
        
        best_neighbor = None
        best_cost = current_cost
        
        for neighbor in neighbors:
            neighbor_cost = get_misplaced_tiles_cost_fn(neighbor)
            if neighbor_cost < best_cost:
                best_cost = neighbor_cost
                best_neighbor = neighbor
                
        if best_neighbor is not None:
            current = best_neighbor
            duong.append(current)
            ds_cost.append(best_cost)
        else:
            return duong, so_node, "Không tìm được nước đi (Thất bại)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}

def steepest_ascent_hill_climbing(bat_dau, dich):
    node = chuan_hoa_bat_dau(bat_dau)
    dich_list = chuan_hoa_dich(dich)
    is_belief = la_trang_thai_belief(node)

    if is_belief:
        def check_goal_fn(st):
            for g in dich_list:
                if all(s == g for s in st):
                    return True
            return False
        def get_successors_fn(st):
            successors = []
            for action in ["U", "D", "L", "R"]:
                next_belief = tuple(apply_action(s, action) for s in st)
                successors.append(next_belief)
            return successors
        def get_heuristic_fn(st):
            min_dist = float('inf')
            for g in dich_list:
                dist = sum(manhattan_distance(s, g) for s in st)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
    else:
        dich_tuple = dich_list[0]
        def check_goal_fn(st):
            return st == dich_tuple
        def get_successors_fn(st):
            return tao_con(st)
        def get_heuristic_fn(st):
            return manhattan_distance(st, dich_tuple)
            
    current = node
    duong = [current]
    c_start = get_heuristic_fn(current)
    ds_cost = [c_start]
    so_node = 0
    
    while True:
        so_node += 1
        if check_goal_fn(current):
            return duong, so_node, "Tìm thấy", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
        neighbors = get_successors_fn(current)
        current_cost = get_heuristic_fn(current)
        
        best_neighbor = None
        best_cost = current_cost
        
        for neighbor in neighbors:
            neighbor_cost = get_heuristic_fn(neighbor)
            if neighbor_cost < best_cost:
                best_cost = neighbor_cost
                best_neighbor = neighbor
                
        if best_neighbor is not None:
            current = best_neighbor
            duong.append(current)
            ds_cost.append(best_cost)
        else:
            return duong, so_node, "Không tìm được nước đi (Thất bại)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}

def stochastic_hill_climbing(bat_dau, dich):
    node = chuan_hoa_bat_dau(bat_dau)
    dich_list = chuan_hoa_dich(dich)
    is_belief = la_trang_thai_belief(node)

    if is_belief:
        def check_goal_fn(st):
            for g in dich_list:
                if all(s == g for s in st):
                    return True
            return False
        def get_successors_fn(st):
            successors = []
            for action in ["U", "D", "L", "R"]:
                next_belief = tuple(apply_action(s, action) for s in st)
                successors.append(next_belief)
            return successors
        def get_heuristic_fn(st):
            min_dist = float('inf')
            for g in dich_list:
                dist = sum(manhattan_distance(s, g) for s in st)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
    else:
        dich_tuple = dich_list[0]
        def check_goal_fn(st):
            return st == dich_tuple
        def get_successors_fn(st):
            return tao_con(st)
        def get_heuristic_fn(st):
            return manhattan_distance(st, dich_tuple)
            
    current = node
    duong = [current]
    c_start = get_heuristic_fn(current)
    ds_cost = [c_start]
    so_node = 0
    
    while True:
        so_node += 1
        if check_goal_fn(current):
            return duong, so_node, "Tìm thấy", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
            
        neighbors = get_successors_fn(current)
        current_cost = get_heuristic_fn(current)
        
        better_neighbors = []
        for neighbor in neighbors:
            neighbor_cost = get_heuristic_fn(neighbor)
            if neighbor_cost < current_cost:
                better_neighbors.append((neighbor, neighbor_cost))
                
        if better_neighbors:
            next_state, next_cost = random.choice(better_neighbors)
            current = next_state
            duong.append(current)
            ds_cost.append(next_cost)
        else:
            return duong, so_node, "Không tìm được nước đi (Thất bại)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}

def random_restart_hill_climbing(bat_dau, dich, max_restart=50):
    node = chuan_hoa_bat_dau(bat_dau)
    dich_list = chuan_hoa_dich(dich)
    is_belief = la_trang_thai_belief(node)

    if is_belief:
        def check_goal_fn(st):
            for g in dich_list:
                if all(s == g for s in st):
                    return True
            return False
        def get_successors_fn(st):
            successors = []
            for action in ["U", "D", "L", "R"]:
                next_belief = tuple(apply_action(s, action) for s in st)
                successors.append(next_belief)
            return successors
        def get_heuristic_fn(st):
            min_dist = float('inf')
            for g in dich_list:
                dist = sum(manhattan_distance(s, g) for s in st)
                if dist < min_dist:
                    min_dist = dist
            return min_dist
    else:
        dich_tuple = dich_list[0]
        def check_goal_fn(st):
            return st == dich_tuple
        def get_successors_fn(st):
            return tao_con(st)
        def get_heuristic_fn(st):
            return manhattan_distance(st, dich_tuple)
            
    tong_node = 0
    best_run_path = None
    best_run_cost = float('inf')
    c_start = get_heuristic_fn(node)
    
    for i in range(1, max_restart + 1):
        current = node
        duong = [current]
        ds_cost = [c_start]
        
        while True:
            tong_node += 1
            if check_goal_fn(current):
                return duong, tong_node, f"Tìm thấy (ở lượt restart {i})", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
                
            neighbors = get_successors_fn(current)
            current_cost = get_heuristic_fn(current)
            
            better_neighbors = []
            for neighbor in neighbors:
                neighbor_cost = get_heuristic_fn(neighbor)
                if neighbor_cost < current_cost:
                    better_neighbors.append((neighbor, neighbor_cost))
                    
            if better_neighbors:
                next_state, next_cost = random.choice(better_neighbors)
                current = next_state
                duong.append(current)
                ds_cost.append(next_cost)
            else:
                if ds_cost[-1] < best_run_cost:
                    best_run_cost = ds_cost[-1]
                    best_run_path = (duong, ds_cost)
                break
                
    if best_run_path:
        duong, ds_cost = best_run_path
        return duong, tong_node, f"Thất bại (sau {max_restart} lượt restart)", {"cost": ds_cost[-1], "values": ds_cost, "history_h": ds_cost}
    return [node], tong_node, f"Thất bại (sau {max_restart} lượt restart)", {"cost": c_start, "values": [c_start], "history_h": [c_start]}
