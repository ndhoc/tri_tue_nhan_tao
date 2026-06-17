from .common import bind_search_functions

def depth_limited_search(bat_dau, dich, gioi_han, is_belief, check_goal_fn, get_successors_fn):
    node = bat_dau
    dich_list = dich

    frontier = [(node, [node], 0)]
    so_node = 0
    bi_cat = False

    while frontier:
        node, duong, do_sau = frontier.pop()
        so_node += 1
        if check_goal_fn(node): 
            return duong, so_node, "found", {"depth": len(duong) - 1, "values_depth": list(range(len(duong))), "values": list(range(len(duong)))}
        
        if do_sau >= gioi_han: 
            bi_cat = True
        else:
            for child in get_successors_fn(node):
                if child not in duong:
                    frontier.append((child, duong + [child], do_sau + 1))
    
    if bi_cat: return None, so_node, "cutoff", {}
    return None, so_node, "failure", {}

def ids(bat_dau, dich):
    node, dich_list, is_belief, check_goal_fn, get_successors_fn, _ = bind_search_functions(bat_dau, dich)

    tong_node = 0
    max_depth = 40

    for depth in range(max_depth + 1):
        duong, so_node, trang_thai, extra = depth_limited_search(node, dich_list, depth, is_belief, check_goal_fn, get_successors_fn)
        tong_node += so_node

        if trang_thai == "found":
            return duong, tong_node, f"Tìm thấy (depth = {depth})", extra
        if trang_thai == "failure":
            return None, tong_node, "Không tìm thấy", {}
            
    return None, tong_node, f"Không tìm thấy (max depth = {max_depth})", {}
