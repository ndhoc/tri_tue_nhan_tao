import sys
import random

def min_conflicts(bat_dau, dich, max_steps=1000):
    """
    Thuật toán Min-Conflicts cho CSP 8-puzzle.
    """
    if isinstance(dich, (list, tuple)) and len(dich) > 0:
        first = dich[0]
        if isinstance(first, (list, tuple)) and len(first) > 0:
            if isinstance(first[0], (list, tuple)):
                goal_grid = dich[0]
            else:
                goal_grid = dich
        else:
            goal_grid = dich
    else:
        goal_grid = dich

    goal_flat = []
    for row in goal_grid:
        for val in row:
            goal_flat.append(val)

    steps = []
    assignment_log = []
    so_node = 0

    def grid_from_current(curr):
        return tuple(tuple(curr[r * 3:(r + 1) * 3]) for r in range(3))

    # Khởi tạo ngẫu nhiên
    current = [random.choice(range(9)) for _ in range(9)]
    steps.append(grid_from_current(current))

    def conflicts(var, value, current_state):
        c = 0
        for i in range(9):
            if i != var and current_state[i] == value:
                c += 1
        if value != goal_flat[var]:
            c += 1
        return c

    for step_idx in range(max_steps):
        so_node += 1
        
        # Tìm các biến bị xung đột
        conflicted_vars = []
        for i in range(9):
            if conflicts(i, current[i], current) > 0:
                conflicted_vars.append(i)

        if not conflicted_vars:
            # Giải xong
            break

        var = random.choice(conflicted_vars)
        
        # Tìm giá trị minimize conflicts
        min_c = float('inf')
        best_vals = []
        for v in range(9):
            c = conflicts(var, v, current)
            if c < min_c:
                min_c = c
                best_vals = [v]
            elif c == min_c:
                best_vals.append(v)
                
        value = random.choice(best_vals)
        
        current[var] = value
        assignment_log.append((var, value))
        steps.append(grid_from_current(current))

    final_grid = grid_from_current(current)
    if steps[-1] != final_grid:
        steps.append(final_grid)

    status = "Tìm thấy" if not conflicted_vars else "Thất bại (vượt max_steps)"
    
    return steps, so_node, status, {
        "cost": len(steps) - 1,
        "values": list(range(len(steps))),
        "assignment_log": assignment_log
    }
