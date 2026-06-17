import sys
import random

sys.setrecursionlimit(5000)


def backtracking_search(bat_dau, dich):
    """
    Thuật toán Backtracking Search phong cách CSP cho 8-puzzle.

    Mô hình CSP:
    - Variables: x_1, x_2, ..., x_9 (9 ô trên bảng 3x3, theo thứ tự hàng)
    - Domain: D = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    - Constraints:
        1. AllDiff: mỗi x_i nhận giá trị khác nhau (x_i != x_j với i != j)
        2. Goal: assignment cuối cùng phải khớp với goal state
    """

    # Chuẩn hóa goal thành dạng phẳng (flat list 9 phần tử)
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

    # CSP setup
    n = 9
    domain = list(range(9))

    so_node = 0
    steps = []
    # Lưu thông tin gán biến tại mỗi bước: (var_index, value)
    assignment_log = []

    def select_unassigned_variable(assignment):
        """Chọn ngẫu nhiên một biến chưa được gán (trừ những x_i đã gán)"""
        unassigned = [i for i in range(n) if i not in assignment]
        return random.choice(unassigned)

    def order_domain_values(var, assignment):
        return list(domain)

    def is_consistent(var, value, assignment):
        if value in assignment.values():
            return False
        if value != goal_flat[var]:
            return False
        return True

    def backtrack(assignment):
        nonlocal so_node

        so_node += 1

        current_grid = assignment_to_grid(assignment)
        steps.append(current_grid)

        if len(assignment) == n:
            return assignment

        var = select_unassigned_variable(assignment)

        for value in order_domain_values(var, assignment):
            if is_consistent(var, value, assignment):
                assignment[var] = value
                assignment_log.append((var, value))

                result = backtrack(assignment)
                if result != "failure":
                    return result

                del assignment[var]

        return "failure"

    def assignment_to_grid(assignment):
        flat = []
        for i in range(n):
            if i in assignment:
                flat.append(assignment[i])
            else:
                flat.append(-1)
        grid = tuple(
            tuple(flat[r * 3:(r + 1) * 3])
            for r in range(3)
        )
        return grid

    # ===== BẮT ĐẦU GIẢI =====
    initial_assignment = {}
    result = backtrack(initial_assignment)

    if result != "failure":
        final_grid = assignment_to_grid(result)
        if steps[-1] != final_grid:
            steps.append(final_grid)

        return steps, so_node, "Tìm thấy", {
            "cost": len(steps) - 1,
            "values": list(range(len(steps))),
            "assignment_log": assignment_log
        }
    else:
        return None, so_node, "Không tìm thấy", {}
