from .common import bind_search_functions
import sys

sys.setrecursionlimit(2000)

def backtracking_search(bat_dau, dich):
    """
    Thuật toán Backtracking Search phong cách CSP cho 8-puzzle.
    """
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, _ = bind_search_functions(bat_dau, dich)
    
    so_node = 0
    
    def select_unassigned_variable(assignment):
        # Biến tiếp theo là chỉ số bước tiếp theo trong chuỗi gán
        return len(assignment)
        
    def order_domain_values(var, assignment):
        # Domain của biến var là các trạng thái con sinh ra từ trạng thái gán ở bước var-1
        prev_state = assignment[var - 1]
        return get_successors_fn(prev_state)
        
    def consistent(var, value, assignment):
        # Trạng thái con không được trùng lặp với các trạng thái đã gán trước đó (tránh chu trình)
        return value not in assignment.values()
        
    def backtrack(assignment):
        nonlocal so_node
        
        curr_var = len(assignment) - 1
        curr_state = assignment[curr_var]
        so_node += 1
        
        # if assignment is complete then return assignment
        if check_goal_fn(curr_state):
            return assignment
            
        # Giới hạn độ sâu
        if len(assignment) >= 40:
            return "failure"
            
        var = select_unassigned_variable(assignment)
        for value in order_domain_values(var, assignment):
            if consistent(var, value, assignment):
                # add {var = value} to assignment
                assignment[var] = value
                
                result = backtrack(assignment)
                if result != "failure":
                    return result
                    
                # remove {var = value} from assignment
                del assignment[var]
        return "failure"

    # Khởi tạo assignment rỗng: gán trạng thái bắt đầu cho biến 0 (bước 0)
    initial_assignment = {0: node}
    res = backtrack(initial_assignment)
    
    if res != "failure":
        path = [res[i] for i in sorted(res.keys())]
        return path, so_node, "Tìm thấy", {"cost": len(path) - 1, "values": list(range(len(path)))}
    else:
        return None, so_node, "Không tìm thấy", {}
