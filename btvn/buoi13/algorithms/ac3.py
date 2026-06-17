import sys

def ac3(bat_dau, dich):
    """
    Thuật toán AC-3 cho CSP 8-puzzle.
    - Variables: x_1, x_2, ..., x_9
    - Domain: D = {0, 1, 2, ..., 8}
    - Constraints: AllDiff và Goal
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

    domain = {i: list(range(9)) for i in range(9)}
    steps = []
    assignment_log = []
    so_node = 0

    def grid_from_domains(dom):
        flat = []
        for i in range(9):
            if len(dom[i]) == 1:
                flat.append(dom[i][0])
            else:
                flat.append(-1)
        grid = tuple(tuple(flat[r * 3:(r + 1) * 3]) for r in range(3))
        return grid

    steps.append(grid_from_domains(domain))

    # Trong AC-3, chúng ta có thể áp dụng Unary constraint (Goal) để giảm domain
    # Ở đây ta sẽ mô phỏng việc apply unary constraint từ từ để trực quan hóa
    for i in range(9):
        so_node += 1
        domain[i] = [goal_flat[i]]
        assignment_log.append((i, goal_flat[i]))
        steps.append(grid_from_domains(domain))

    queue = [(i, j) for i in range(9) for j in range(9) if i != j]

    while queue:
        so_node += 1
        i, j = queue.pop(0)

        # Remove inconsistent values
        removed = False
        new_di = []
        for x in domain[i]:
            # Consistent if there's any y in domain[j] such that x != y
            if any(x != y for y in domain[j]):
                new_di.append(x)
            else:
                removed = True

        if removed:
            domain[i] = new_di
            if len(domain[i]) == 1:
                assignment_log.append((i, domain[i][0]))
                steps.append(grid_from_domains(domain))

            for k in range(9):
                if k != i and k != j:
                    queue.append((k, i))

    final_grid = grid_from_domains(domain)
    if steps[-1] != final_grid:
        steps.append(final_grid)

    return steps, so_node, "Tìm thấy", {
        "cost": len(steps) - 1,
        "values": list(range(len(steps))),
        "assignment_log": assignment_log
    }
