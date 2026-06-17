import random
import math
from .common import doi_tuple, tao_con, manhattan_distance, tim_so_0

def apply_action(state, action):
    a = [list(row) for row in state]
    x, y = tim_so_0(a)
    dx, dy = x, y
    if action == "U": dx = x - 1
    elif action == "D": dx = x + 1
    elif action == "L": dy = y - 1
    elif action == "R": dy = y + 1
    
    if 0 <= dx < 3 and 0 <= dy < 3:
        a[x][y], a[dx][dy] = a[dx][dy], a[x][y]
        return tuple(tuple(row) for row in a)
    return state

def simulated_annealing(bat_dau, dich, T0=100.0, Tmin=0.05, alpha=0.995, max_steps=2000):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    current = node
    path = [current]
    
    T = T0
    so_node = 0
    
    h_curr = manhattan_distance(current, dich_tuple)
    history_h = [h_curr]
    history_T = [T]
    
    while T > Tmin and so_node < max_steps:
        if current == dich_tuple:
            return path, so_node, "Tìm thấy", {
                "cost": len(path) - 1,
                "values": history_h,
                "history_h": history_h,
                "history_T": history_T,
                "steps": so_node
            }
            
        so_node += 1
        neighbors = tao_con(current)
        next_state = random.choice(neighbors)
        
        h_next = manhattan_distance(next_state, dich_tuple)
        delta = h_next - h_curr
        
        if delta < 0:
            current = next_state
            h_curr = h_next
            path.append(current)
            history_h.append(h_curr)
            history_T.append(T)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current = next_state
                h_curr = h_next
                path.append(current)
                history_h.append(h_curr)
                history_T.append(T)
                
        T = alpha * T
        
    if current == dich_tuple:
        return path, so_node, "Tìm thấy", {
            "cost": len(path) - 1,
            "values": history_h,
            "history_h": history_h,
            "history_T": history_T,
            "steps": so_node
        }
        
    return path, so_node, "Thất bại (Hết nhiệt độ/Số bước)", {
        "cost": len(path) - 1,
        "values": history_h,
        "history_h": history_h,
        "history_T": history_T,
        "steps": so_node
    }

def simulated_annealing_belief(bat_dau_list, dich_list, T0=100.0, Tmin=0.05, alpha=0.995, max_steps=2000):
    starts = sorted([doi_tuple(s) for s in bat_dau_list])
    goals = [doi_tuple(g) for g in dich_list]
    
    current_belief = tuple(starts)
    path = [current_belief]
    actions_taken = []
    
    T = T0
    so_node = 0
    
    def h(belief):
        min_dist = float('inf')
        for g in goals:
            dist = sum(manhattan_distance(s, g) for s in belief)
            if dist < min_dist:
                min_dist = dist
        return min_dist

    def is_goal(belief):
        for g in goals:
            if all(s == g for s in belief):
                return True
        return False

    h_curr = h(current_belief)
    history_h = [h_curr]
    history_T = [T]
    
    while T > Tmin and so_node < max_steps:
        if is_goal(current_belief):
            return path, actions_taken, so_node, "Tìm thấy", {
                "cost": len(actions_taken),
                "values": history_h,
                "history_h": history_h,
                "history_T": history_T,
                "steps": so_node
            }
            
        so_node += 1
        action = random.choice(["U", "D", "L", "R"])
        next_belief = tuple(sorted(apply_action(s, action) for s in current_belief))
        
        h_next = h(next_belief)
        delta = h_next - h_curr
        
        if delta < 0:
            current_belief = next_belief
            h_curr = h_next
            path.append(current_belief)
            actions_taken.append(action)
            history_h.append(h_curr)
            history_T.append(T)
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                current_belief = next_belief
                h_curr = h_next
                path.append(current_belief)
                actions_taken.append(action)
                history_h.append(h_curr)
                history_T.append(T)
                
        T = alpha * T
        
    if is_goal(current_belief):
        return path, actions_taken, so_node, "Tìm thấy", {
            "cost": len(actions_taken),
            "values": history_h,
            "history_h": history_h,
            "history_T": history_T,
            "steps": so_node
        }
        
    return path, actions_taken, so_node, "Thất bại (Hết nhiệt độ/Số bước)", {
        "cost": len(actions_taken),
        "values": history_h,
        "history_h": history_h,
        "history_T": history_T,
        "steps": so_node
    }
