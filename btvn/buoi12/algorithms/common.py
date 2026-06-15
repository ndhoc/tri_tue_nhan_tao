import random
import threading

class SearchCancelledException(Exception):
    pass

cancelled_threads = set()
cancel_check_counter = 0

def check_cancelled():
    global cancel_check_counter
    cancel_check_counter += 1
    if cancel_check_counter % 128 == 0:
        if threading.current_thread().name in cancelled_threads:
            raise SearchCancelledException("Search cancelled by user closing the window.")

def rule(x, y):
    moves = []
    if (x == 0 and y == 0): moves = [(0, 1), (1, 0)]
    elif (x == 0 and y == 1): moves = [(0, 0), (0, 2), (1, 1)]
    elif (x == 0 and y == 2): moves = [(0, 1), (1, 2)]
    elif (x == 1 and y == 0): moves = [(0, 0), (1, 1), (2, 0)]
    elif (x == 1 and y == 1): moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
    elif (x == 1 and y == 2): moves = [(0, 2), (1, 1), (2, 2)]
    elif (x == 2 and y == 0): moves = [(1, 0), (2, 1)]
    elif (x == 2 and y == 1): moves = [(1, 1), (2, 0), (2, 2)]
    else: moves = [(2, 1), (1, 2)]
    return moves

def tim_so_0(a):
    for i in range(3):
        for j in range(3):
            if (a[i][j] == 0):
                return i, j
    return -1, -1

def doi_tuple(a):
    return tuple(tuple(row) for row in a)

def doi_list(a):
    return [list(row) for row in a]

def dem_nghich_the(a):
    b = [a[i][j] for i in range(3) for j in range(3) if a[i][j] != 0]
    dem = 0
    for i in range(len(b)):
        for j in range(i + 1, len(b)):
            if (b[i] > b[j]):
                dem += 1
    return dem

def co_giai_duoc(a):
    return dem_nghich_the(a) % 2 == 0

def sinh_ma_tran():
    so = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while True:
        random.shuffle(so)
        a = [so[i*3:(i+1)*3] for i in range(3)]
        if co_giai_duoc(a):
            return a

def tao_con(trang_thai):
    check_cancelled()
    a = doi_list(trang_thai)
    x, y = tim_so_0(a)
    ds_con = []
    for dx, dy in rule(x, y):
        b = doi_list(trang_thai)
        b[x][y], b[dx][dy] = b[dx][dy], b[x][y]
        ds_con.append(doi_tuple(b))
    return ds_con

def apply_action(state, action):
    check_cancelled()
    a = [list(row) for row in state]
    x, y = tim_so_0(a)
    dx, dy = x, y
    if action == "U": dx = x - 1
    elif action == "D": dx = x + 1
    elif action == "L": dy = y - 1
    elif action == "R": dy = y + 1
    
    if 0 <= dx < 3 and 0 <= dy < 3:
        a[x][y], a[dx][dy] = a[dx][dy], a[x][y]
        return doi_tuple(a)
    return state

def la_trang_thai_belief(state):
    if isinstance(state, tuple) and len(state) > 0:
        first = state[0]
        if isinstance(first, tuple) and len(first) > 0:
            return isinstance(first[0], tuple)
    return False

def get_successors(state):
    if la_trang_thai_belief(state):
        successors = []
        for action in ["U", "D", "L", "R"]:
            next_belief = tuple(apply_action(s, action) for s in state)
            successors.append(next_belief)
        return successors
    else:
        return tao_con(state)

def check_goal(state, goals):
    # goals is a list/tuple of goal physical states
    if la_trang_thai_belief(state):
        for g in goals:
            if all(s == g for s in state):
                return True
        return False
    else:
        return state in goals

def get_heuristic(state, goals):
    if la_trang_thai_belief(state):
        min_dist = float('inf')
        for g in goals:
            dist = sum(manhattan_distance(s, g) for s in state)
            if dist < min_dist:
                min_dist = dist
        return min_dist
    else:
        return manhattan_distance(state, goals[0])

def get_misplaced_tiles_cost(state, goals):
    if la_trang_thai_belief(state):
        min_dist = float('inf')
        for g in goals:
            dist = sum(dem_o_sai_khong_tinh_0(s, g) for s in state)
            if dist < min_dist:
                min_dist = dist
        return min_dist
    else:
        return dem_o_sai_khong_tinh_0(state, goals[0])

def get_misplaced_tiles_cost_with_0(state, goals):
    if la_trang_thai_belief(state):
        min_dist = float('inf')
        for g in goals:
            dist = sum(dem_o_sai(s, g) for s in state)
            if dist < min_dist:
                min_dist = dist
        return min_dist
    else:
        return dem_o_sai(state, goals[0])

def huong_di_chuyen(truoc, sau):
    # If belief states, find the action that transitions truoc to sau
    if la_trang_thai_belief(truoc):
        for action in ["U", "D", "L", "R"]:
            candidate = tuple(sorted(apply_action(s, action) for s in truoc))
            if candidate == sau:
                return action
        return "?"
    a = doi_list(truoc)
    b = doi_list(sau)
    x1, y1 = tim_so_0(a)
    x2, y2 = tim_so_0(b)
    if (x2 == x1 - 1 and y2 == y1): return "U"
    elif (x2 == x1 + 1 and y2 == y1): return "D"
    elif (x2 == x1 and y2 == y1 - 1): return "L"
    elif (x2 == x1 and y2 == y1 + 1): return "R"
    return "?"

def giai_thich_huong(huong):
    huong_dict = {"U": "Up", "D": "Down", "L": "Left", "R": "Right"}
    return huong_dict.get(huong, "Unknown")

def doi_trang_thai_thanh_chuoi(trang_thai):
    a = doi_list(trang_thai)
    chuoi = ""
    for i in range(3):
        for j in range(3):
            if a[i][j] == 0:
                chuoi += "_ "
            else:
                chuoi += str(a[i][j]) + " "
        chuoi += "\n"
    return chuoi

def manhattan_distance(state, goal):
    check_cancelled()
    dist = 0
    for num in range(1, 9):
        c_r, c_c = -1, -1
        for i in range(3):
            for j in range(3):
                if state[i][j] == num:
                    c_r, c_c = i, j
                    break
            if c_r != -1: break
            
        g_r, g_c = -1, -1
        for i in range(3):
            for j in range(3):
                if goal[i][j] == num:
                    g_r, g_c = i, j
                    break
            if g_r != -1: break
            
        dist += abs(c_r - g_r) + abs(c_c - g_c)
    return dist

def dem_o_sai(state, goal):
    dem = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                dem += 1
    return dem

def dem_o_sai_khong_tinh_0(state, goal):
    dem = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                dem += 1
    return dem

def chuan_hoa_bat_dau(bat_dau):
    if la_trang_thai_belief(bat_dau):
        return tuple(sorted(doi_tuple(s) for s in bat_dau))
    return doi_tuple(bat_dau)

def chuan_hoa_dich(dich):
    if isinstance(dich, (list, tuple)) and len(dich) > 0:
        first = dich[0]
        if isinstance(first, (list, tuple)) and len(first) > 0:
            if isinstance(first[0], (list, tuple)) and len(first[0]) > 0:
                return [doi_tuple(g) for g in dich]
    return [doi_tuple(dich)]

def bind_search_functions(bat_dau, dich):
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
                next_belief = tuple(sorted(apply_action(s, action) for s in st))
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
            
    return node, dich_list, is_belief, check_goal_fn, get_successors_fn, get_heuristic_fn


