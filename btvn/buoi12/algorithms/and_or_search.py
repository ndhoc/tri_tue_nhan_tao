from .common import bind_search_functions, huong_di_chuyen
import sys

sys.setrecursionlimit(2000)

def and_or_graph_search(bat_dau, dich):
    """
    Thuật toán AND-OR Graph Search cho 8-puzzle sử dụng cấu trúc gán trạng thái của visualizer.
    """
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, _ = bind_search_functions(bat_dau, dich)
    
    so_node = 0
    
    def OR_SEARCH(state, path):
        nonlocal so_node
        so_node += 1
        
        if check_goal_fn(state):
            return []
            
        if state in path:
            return "failure"
            
        if len(path) >= 30:
            return "failure"
            
        for child in get_successors_fn(state):
            action = huong_di_chuyen(state, child)
            result_states = [child]
            
            plan = AND_SEARCH(result_states, path + [state])
            if plan != "failure":
                return [action, plan]
        return "failure"
        
    def AND_SEARCH(states, path):
        plans = {}
        for s in states:
            plan_s = OR_SEARCH(s, path)
            if plan_s == "failure":
                return "failure"
            plans[s] = plan_s
        return plans

    plan = OR_SEARCH(node, [])
    
    if plan == "failure":
        return None, so_node, "Không tìm thấy", {}
        
    def rebuild_path(state, p):
        if p == []:
            return [state]
        action, plans_dict = p
        next_state = list(plans_dict.keys())[0]
        return [state] + rebuild_path(next_state, plans_dict[next_state])
        
    path = rebuild_path(node, plan)
    return path, so_node, "Tìm thấy", {"cost": len(path) - 1, "values": list(range(len(path)))}
