import sys
import random

sys.setrecursionlimit(5000)


def forward_checking_search(bat_dau, dich):
    """
    Thuật toán Forward Checking cho 8-puzzle dưới dạng CSP.

    Giống Backtracking nhưng thêm bước Forward Checking:
    - Sau khi gán assignment cho biến var
    - Loại bỏ khỏi domain những giá trị không hợp lệ nữa
    - Cập nhật lại domain D
    - Nếu domain rỗng -> backtracking

    Mô hình CSP:
    - Variables: x_1, x_2, ..., x_9 (9 ô trên bảng 3x3)
    - Domain: D = {0, 1, 2, 3, 4, 5, 6, 7, 8}
    - Constraints:
        1. AllDiff: mỗi x_i nhận giá trị khác nhau
        2. Goal: assignment cuối cùng phải khớp với goal state
    """

    # Chuẩn hóa goal thành dạng phẳng
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
    so_node = 0
    steps = []
    assignment_log = []

    def select_unassigned_variable(assignment):
        """Chọn ngẫu nhiên một biến chưa được gán (trừ những x_i đã gán)"""
        unassigned = [i for i in range(n) if i not in assignment]
        return random.choice(unassigned)

    def order_domain_values(var, domains):
        return list(domains[var])

    def is_consistent(var, value, assignment):
        if value in assignment.values():
            return False
        if value != goal_flat[var]:
            return False
        return True

    def forward_check(var, value, assignment, domains):
        new_domains = {}
        for i in range(n):
            new_domains[i] = set(domains[i])

        for future_var in range(n):
            if future_var in assignment or future_var == var:
                continue

            # Ràng buộc AllDiff
            if value in new_domains[future_var]:
                new_domains[future_var].discard(value)

            # Ràng buộc Goal
            vals_to_remove = [v for v in new_domains[future_var] if v != goal_flat[future_var]]
            for v in vals_to_remove:
                new_domains[future_var].discard(v)

            if len(new_domains[future_var]) == 0:
                return None

        return new_domains

    def backtrack(assignment, domains):
        nonlocal so_node

        so_node += 1

        current_grid = assignment_to_grid(assignment)
        steps.append(current_grid)

        if len(assignment) == n:
            return assignment

        var = select_unassigned_variable(assignment)

        for value in order_domain_values(var, domains):
            if is_consistent(var, value, assignment):
                assignment[var] = value
                assignment_log.append((var, value))

                new_domains = forward_check(var, value, assignment, domains)

                if new_domains is not None:
                    result = backtrack(assignment, new_domains)
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
    initial_domains = {}
    for i in range(n):
        initial_domains[i] = set(range(9))

    initial_assignment = {}
    result = backtrack(initial_assignment, initial_domains)

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
