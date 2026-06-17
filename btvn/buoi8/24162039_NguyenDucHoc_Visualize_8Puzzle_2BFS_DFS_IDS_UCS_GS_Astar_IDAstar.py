import random
import tkinter as tk
from tkinter import ttk
from queue import Queue, PriorityQueue
import heapq
import threading

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
    a = doi_list(trang_thai)
    x, y = tim_so_0(a)
    ds_con = []
    for dx, dy in rule(x, y):
        b = doi_list(trang_thai)
        b[x][y], b[dx][dy] = b[dx][dy], b[x][y]
        ds_con.append(doi_tuple(b))
    return ds_con

def huong_di_chuyen(truoc, sau):
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

def bfs_phien_ban_1(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)

    frontier = Queue()
    frontier.put((node, [node]))
    frontier_set = {node}
    explored = set()
    so_node = 0

    while not frontier.empty():
        node, duong = frontier.get()
        frontier_set.remove(node)
        so_node += 1
        
        if node == dich_tuple: 
            return duong, so_node, "Tìm thấy", {"cost": len(duong) - 1, "values": list(range(len(duong)))}
        
        explored.add(node)
        
        for child in tao_con(node):
            if child not in explored and child not in frontier_set:
                frontier.put((child, duong + [child]))
                frontier_set.add(child)
    return None, so_node, "Không tìm thấy", {}

def bfs_phien_ban_2(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    if node == dich_tuple: 
        return [node], 1, "Tìm thấy", {"cost": 0, "values": [0]}
    
    frontier = Queue()
    frontier.put((node, [node]))
    frontier_set = {node}
    explored = set()
    so_node = 0

    while not frontier.empty():
        node, duong = frontier.get()
        frontier_set.remove(node)
        so_node += 1
        explored.add(node)

        for child in tao_con(node):
            if child not in explored and child not in frontier_set:
                if child == dich_tuple:
                    return duong + [child], so_node, "Tìm thấy", {"cost": len(duong), "values": list(range(len(duong) + 1))}
                frontier.put((child, duong + [child]))
                frontier_set.add(child)
    return None, so_node, "Không tìm thấy", {}

def dfs(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    if node == dich_tuple: return [node], 1, "Tìm thấy", {"cost": 0, "values": [0]}

    frontier = [(node, [node])]
    reached = {node}
    so_node = 0

    while frontier:
        node, duong = frontier.pop()
        so_node += 1
        if node == dich_tuple: return duong, so_node, "Tìm thấy", {"cost": len(duong) - 1, "values": list(range(len(duong)))}
        
        for child in tao_con(node):
            if child == dich_tuple:
                return duong + [child], so_node, "Tìm thấy", {"cost": len(duong), "values": list(range(len(duong) + 1))}
            if child not in reached:
                reached.add(child)
                frontier.append((child, duong + [child]))
    return None, so_node, "Không tìm thấy", {}

def depth_limited_search(bat_dau, dich, gioi_han):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)

    frontier = [(node, [node], 0)]
    so_node = 0
    bi_cat = False

    while frontier:
        node, duong, do_sau = frontier.pop()
        so_node += 1
        if node == dich_tuple: return duong, so_node, "found", {"depth": len(duong) - 1, "values_depth": list(range(len(duong)))}
        
        if do_sau >= gioi_han: 
            bi_cat = True
        else:
            for child in tao_con(node):
                if child not in duong:
                    frontier.append((child, duong + [child], do_sau + 1))
    
    if bi_cat: return None, so_node, "cutoff", {}
    return None, so_node, "failure", {}

def ids(bat_dau, dich):
    tong_node = 0
    max_depth = 40

    for depth in range(max_depth + 1):
        duong, so_node, trang_thai, extra = depth_limited_search(bat_dau, dich, depth)
        tong_node += so_node

        if trang_thai == "found":
            return duong, tong_node, f"Tìm thấy (depth = {depth})", extra
        if trang_thai == "failure":
            return None, tong_node, "Không tìm thấy", {}
            
    return None, tong_node, f"Không tìm thấy (max depth = {max_depth})", {}

def ucs(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)

    if node == dich_tuple: 
        return [node], 1, "Tìm thấy", {"cost": 0, "values": [0]}

    counter = 0
    frontier = []
    heapq.heappush(frontier, (0, counter, node, [node], [0]))
    
    best_cost = {node: 0}
    so_node = 0

    while frontier:
        cost, _, current_node, duong, ds_cost = heapq.heappop(frontier)
        so_node += 1

        if current_node == dich_tuple: 
            return duong, so_node, "Tìm thấy", {"cost": cost, "values": ds_cost}

        ds_con = tao_con(current_node)
        so_con_parent = len(ds_con)
        
        for child in ds_con:
            depth_child = len(duong)
            step_cost = depth_child + so_con_parent
            new_cost = cost + step_cost

            if child not in best_cost or new_cost < best_cost[child]:
                best_cost[child] = new_cost
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, child, duong + [child], ds_cost + [new_cost]))

    return None, so_node, "Không tìm thấy", {}

def manhattan_distance(state, goal):
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

def greedy_search(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    h_start = manhattan_distance(node, dich_tuple)
    if node == dich_tuple: 
        return [node], 1, "Tìm thấy", {"heuristic": h_start, "values": [h_start]}

    counter = 0
    frontier = []
    heapq.heappush(frontier, (h_start, counter, node, [node], [h_start]))
    
    reached = {node}
    so_node = 0

    while frontier:
        h, _, current_node, duong, ds_h = heapq.heappop(frontier)
        so_node += 1

        if current_node == dich_tuple: 
            return duong, so_node, "Tìm thấy", {"heuristic": 0, "values": ds_h, "h_start": h_start}

        for child in tao_con(current_node):
            if child not in reached:
                reached.add(child)
                h_child = manhattan_distance(child, dich_tuple)
                counter += 1
                heapq.heappush(frontier, (h_child, counter, child, duong + [child], ds_h + [h_child]))

    return None, so_node, "Không tìm thấy", {}

def dem_o_sai(state, goal):
    dem = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                dem += 1
    return dem

def a_star(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    h_start = manhattan_distance(node, dich_tuple)
    if node == dich_tuple:
        return [node], 1, "Tìm thấy", {
            "cost": 0,
            "values": [0],
            "values_g": [0],
            "values_h": [0],
            "values_f": [0]
        }
    
    counter = 0
    frontier = []
    # (f, counter, current_node, path, path_g, path_h, path_f)
    heapq.heappush(frontier, (h_start, counter, node, [node], [0], [h_start], [h_start]))
    
    best_g = {node: 0}
    so_node = 0
    
    while frontier:
        f, _, current_node, path, ds_g, ds_h, ds_f = heapq.heappop(frontier)
        so_node += 1
        
        current_g = ds_g[-1]
        
        if current_node == dich_tuple:
            return path, so_node, "Tìm thấy", {
                "cost": current_g,
                "values": ds_f,
                "values_g": ds_g,
                "values_h": ds_h,
                "values_f": ds_f
            }
            
        if current_g > best_g.get(current_node, float('inf')):
            continue
            
        for child in tao_con(current_node):
            step_cost = dem_o_sai(child, dich_tuple)
            g_child = current_g + step_cost
            h_child = manhattan_distance(child, dich_tuple)
            f_child = g_child + h_child
            
            if child not in best_g or g_child < best_g[child]:
                best_g[child] = g_child
                counter += 1
                heapq.heappush(frontier, (f_child, counter, child, path + [child], ds_g + [g_child], ds_h + [h_child], ds_f + [f_child]))
                
    return None, so_node, "Không tìm thấy", {}

def ida_star(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich_tuple = doi_tuple(dich)
    
    h_start = manhattan_distance(node, dich_tuple)
    if node == dich_tuple:
        return [node], 1, f"Tìm thấy (threshold = {h_start})", {
            "cost": 0,
            "values": [0],
            "values_g": [0],
            "values_h": [0],
            "values_f": [0],
            "threshold": h_start,
            "threshold_history": [h_start]
        }
        
    threshold = h_start
    tong_node = 0
    threshold_history = []
    
    def search(current_node, g_hien_tai, duong, ds_g, ds_h, ds_f):
        nonlocal tong_node
        tong_node += 1
        
        h_val = manhattan_distance(current_node, dich_tuple)
        f_val = g_hien_tai + h_val
        
        if f_val > threshold:
            return f_val, None
            
        if current_node == dich_tuple:
            return "found", (duong, ds_g, ds_h, ds_f)
            
        min_over = float('inf')
        
        for child in tao_con(current_node):
            if child not in duong:
                step_cost = dem_o_sai(child, dich_tuple)
                g_child = g_hien_tai + step_cost
                h_child = manhattan_distance(child, dich_tuple)
                f_child = g_child + h_child
                
                res, val = search(child, g_child, duong + [child], ds_g + [g_child], ds_h + [h_child], ds_f + [f_child])
                
                if res == "found":
                    return "found", val
                if res < min_over:
                    min_over = res
                    
        return min_over, None

    while True:
        threshold_history.append(threshold)
        res, val = search(node, 0, [node], [0], [h_start], [h_start])
        
        if res == "found":
            duong, ds_g, ds_h, ds_f = val
            return duong, tong_node, f"Tìm thấy (threshold = {threshold})", {
                "cost": ds_g[-1],
                "values": ds_f,
                "values_g": ds_g,
                "values_h": ds_h,
                "values_f": ds_f,
                "threshold": threshold,
                "threshold_history": threshold_history
            }
        if res == float('inf'):
            return None, tong_node, "Không tìm thấy", {}
        
        threshold = res

ds_thuat_toan = [
    ("BFS Version 1", bfs_phien_ban_1),
    ("BFS Version 2", bfs_phien_ban_2),
    ("DFS", dfs),
    ("IDS", ids),
    ("UCS", ucs),
    ("Greedy Search", greedy_search),
    ("A*", a_star),
    ("IDA*", ida_star)
]

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Search Algorithm Visualizer")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f6f9")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TFrame", background="#f4f6f9")
        self.style.configure("TLabel", background="#f4f6f9", font=("Segoe UI", 11))

        self.dich = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        
        self.bang = [
            [1, 3, 6],
            [8, 0, 7],
            [2, 5, 4]
        ]

        self.ket_qua = []
        self.thong_tin_phu = {}
        self.buoc = 0
        self.dang_chay = False
        self.dang_tim_kiem = False
        self.toc_do = 700
        self.ten_thuat_toan = ""
        self.ds_nuoc_di = []
        self.buoc_da_log = set()
        
        self.ket_qua_tam = None
        self.ten_tam = ""
        self.root.bind("<<SearchDone>>", self._xu_ly_ket_qua_sau_khi_chay)

        self.setup_ui()
        self.hien_bang(self.bang)
        self.xoa_log()

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#f4f6f9")
        header_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(header_frame, text="8-Puzzle Search Algorithm Visualizer", font=("Segoe UI", 16, "bold"), fg="#1e3a8a", bg="#f4f6f9").pack()
        tk.Label(header_frame, text="Mô phỏng BFS, DFS, IDS, UCS, Greedy Search, A* và IDA*", font=("Segoe UI", 11), fg="#4b5563", bg="#f4f6f9").pack()

        main_frame = tk.Frame(self.root, bg="#f4f6f9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.board_frame = tk.Frame(left_frame, bg="#94a3b8", bd=4, relief="ridge")
        self.board_frame.pack(pady=10)
        
        self.cells = []
        for i in range(3):
            row_cells = []
            for j in range(3):
                lbl = tk.Label(self.board_frame, text="", width=4, height=2, 
                               font=("Segoe UI", 28, "bold"), bg="#ffffff", fg="#1e293b", relief="raised", bd=3)
                lbl.grid(row=i, column=j, padx=3, pady=3)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        self.lbl_result = tk.Label(left_frame, text="Chưa chạy thuật toán", font=("Segoe UI", 12), fg="#047857", bg="#ffffff", wraplength=600, justify="center")
        self.lbl_result.pack(pady=5)

        log_frame = tk.Frame(left_frame, bg="#ffffff")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tk.Label(log_frame, text="Log Hoạt Động", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(anchor=tk.W)
        
        scroll_y = ttk.Scrollbar(log_frame, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x = ttk.Scrollbar(log_frame, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.txt_log = tk.Text(log_frame, height=10, font=("Consolas", 10), bg="#f8fafc", fg="#334155", 
                               wrap="none", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.config(command=self.txt_log.yview)
        scroll_x.config(command=self.txt_log.xview)
        self.txt_log.config(state="disabled")

        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid", width=330)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        canvas = tk.Canvas(right_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        control_inner = tk.Frame(canvas, bg="#ffffff", padx=15, pady=15)
        
        control_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas_win = canvas.create_window((0, 0), window=control_inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

        tk.Label(control_inner, text="Thiết Lập Bài Toán", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(anchor=tk.W, pady=(0, 5))
        self.btn_sinh = tk.Button(control_inner, text="Sinh ma trận ngẫu nhiên", font=("Segoe UI", 10, "bold"), bg="#3b82f6", fg="white", relief="flat", command=self.bam_sinh)
        self.btn_sinh.pack(fill=tk.X, pady=2)
        self.btn_nhap = tk.Button(control_inner, text="Nhập ma trận", font=("Segoe UI", 10, "bold"), bg="#8b5cf6", fg="white", relief="flat", command=self.bam_nhap_ma_tran)
        self.btn_nhap.pack(fill=tk.X, pady=2)
        
        ttk.Separator(control_inner, orient='horizontal').pack(fill=tk.X, pady=10)

        tk.Label(control_inner, text="Chọn Thuật Toán", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(anchor=tk.W, pady=(0, 5))
        self.algo_buttons = []
        for ten, ham in ds_thuat_toan:
            btn = tk.Button(control_inner, text=ten, font=("Segoe UI", 10), bg="#e2e8f0", fg="#1e293b", relief="flat",
                            command=lambda t=ten, h=ham: self.chay_thuat_toan(t, h))
            btn.pack(fill=tk.X, pady=2)
            self.algo_buttons.append(btn)

        ttk.Separator(control_inner, orient='horizontal').pack(fill=tk.X, pady=10)

        tk.Label(control_inner, text="Điều Khiển Mô Phỏng", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(anchor=tk.W, pady=(0, 5))
        
        btn_frame1 = tk.Frame(control_inner, bg="#ffffff")
        btn_frame1.pack(fill=tk.X, pady=2)
        self.btn_truoc = tk.Button(btn_frame1, text="Bước trước", font=("Segoe UI", 10), width=12, bg="#f1f5f9", relief="flat", command=self.bam_truoc)
        self.btn_truoc.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,2))
        self.btn_tiep = tk.Button(btn_frame1, text="Bước sau", font=("Segoe UI", 10), width=12, bg="#f1f5f9", relief="flat", command=self.bam_tiep)
        self.btn_tiep.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2,0))

        self.btn_auto = tk.Button(control_inner, text="Tự động chạy", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", command=self.bam_tu_dong)
        self.btn_auto.pack(fill=tk.X, pady=4)
        
        btn_frame2 = tk.Frame(control_inner, bg="#ffffff")
        btn_frame2.pack(fill=tk.X, pady=2)
        self.btn_dung = tk.Button(btn_frame2, text="Dừng", font=("Segoe UI", 10), width=12, bg="#fca5a5", relief="flat", command=self.bam_dung)
        self.btn_dung.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,2))
        self.btn_xoa_log = tk.Button(btn_frame2, text="Xóa log", font=("Segoe UI", 10), width=12, bg="#fca5a5", relief="flat", command=self.bam_xoa_log_btn)
        self.btn_xoa_log.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2,0))

        tk.Label(control_inner, text="Tốc độ chạy (ms):", font=("Segoe UI", 9), bg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        self.scale_speed = ttk.Scale(control_inner, from_=100, to=2000, orient="horizontal", command=self.doi_toc_do)
        self.scale_speed.set(700)
        self.scale_speed.pack(fill=tk.X, pady=5)

    def doi_toc_do(self, value):
        self.toc_do = int(float(value))

    def hien_bang(self, a):
        for i in range(3):
            for j in range(3):
                if a[i][j] == 0:
                    self.cells[i][j].config(text="", bg="#e2e8f0")
                else:
                    self.cells[i][j].config(text=str(a[i][j]), bg="#ffffff")

    def toggle_buttons(self, state):
        self.btn_sinh.config(state=state)
        for btn in self.algo_buttons:
            btn.config(state=state)
        self.btn_truoc.config(state=state)
        self.btn_tiep.config(state=state)
        self.btn_auto.config(state=state)
        self.btn_dung.config(state=state)

    def bam_sinh(self):
        if self.dang_tim_kiem: return
        self.dang_chay = False
        self.bang = sinh_ma_tran()
        self.ket_qua = []
        self.thong_tin_phu = {}
        self.buoc = 0
        self.ten_thuat_toan = ""
        self.ds_nuoc_di = []
        self.hien_bang(self.bang)
        self.xoa_log()
        self.lbl_result.config(text="Đã sinh ma trận mới. Hãy chọn thuật toán.", fg="#047857")

    def bam_nhap_ma_tran(self):
        if self.dang_tim_kiem: return
        dialog = tk.Toplevel(self.root)
        dialog.title("Nhập ma trận 3x3")
        dialog.geometry("280x220")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        tk.Label(dialog, text="Nhập 9 số (0-8), 0 là ô trống:", font=("Segoe UI", 10)).pack(pady=5)
        
        grid_frame = tk.Frame(dialog)
        grid_frame.pack(pady=5)
        entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                e = tk.Entry(grid_frame, width=4, font=("Segoe UI", 14, "bold"), justify="center")
                e.grid(row=i, column=j, padx=3, pady=3)
                e.insert(0, str(self.bang[i][j]))
                row_entries.append(e)
            entries.append(row_entries)
        
        lbl_err = tk.Label(dialog, text="", font=("Segoe UI", 9), fg="red")
        lbl_err.pack()
        
        def xac_nhan():
            try:
                vals = []
                for i in range(3):
                    row = []
                    for j in range(3):
                        v = int(entries[i][j].get().strip())
                        if v < 0 or v > 8:
                            lbl_err.config(text="Giá trị phải từ 0 đến 8!")
                            return
                        row.append(v)
                    vals.append(row)
                flat = [vals[i][j] for i in range(3) for j in range(3)]
                if sorted(flat) != list(range(9)):
                    lbl_err.config(text="Phải chứa đủ các số 0-8 không trùng!")
                    return
                self.dang_chay = False
                self.bang = vals
                self.ket_qua = []
                self.thong_tin_phu = {}
                self.buoc = 0
                self.ten_thuat_toan = ""
                self.ds_nuoc_di = []
                self.hien_bang(self.bang)
                self.xoa_log()
                self.lbl_result.config(text="Đã nhập ma trận mới. Hãy chọn thuật toán.", fg="#047857")
                dialog.destroy()
            except ValueError:
                lbl_err.config(text="Vui lòng nhập số nguyên!")
        
        tk.Button(dialog, text="Xác nhận", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", command=xac_nhan).pack(pady=5)

    def xoa_log(self):
        self.ds_nuoc_di = []
        self.buoc_da_log = set()
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", tk.END)
        self.txt_log.insert(tk.END, "LOG TRẠNG THÁI DI CHUYỂN\n")
        self.txt_log.insert(tk.END, "Quy ước: L = Left | R = Right | U = Up | D = Down\n")
        self.txt_log.insert(tk.END, "-"*60 + "\n")
        self.txt_log.config(state="disabled")

    def bam_xoa_log_btn(self):
        self.xoa_log()
        self.lbl_result.config(text="Đã xóa log.")

    def them_log_bat_dau(self):
        self.txt_log.config(state="normal")
        log_str = "Bước 0 | START"
        if "values_g" in self.thong_tin_phu and "values_h" in self.thong_tin_phu and "values_f" in self.thong_tin_phu:
            g_val = self.thong_tin_phu["values_g"][0]
            h_val = self.thong_tin_phu["values_h"][0]
            f_val = self.thong_tin_phu["values_f"][0]
            log_str += f" | g(n): {g_val} | h(n): {h_val} | f(n): {f_val}"
        self.txt_log.insert(tk.END, log_str + "\n")
        self.txt_log.insert(tk.END, doi_trang_thai_thanh_chuoi(self.ket_qua[0]))
        self.txt_log.insert(tk.END, "-"*60 + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")
        self.buoc_da_log.add(0)

    def them_log_buoc_di(self):
        if not self.ket_qua or self.buoc <= 0: return
        
        if self.buoc in self.buoc_da_log: return
        self.buoc_da_log.add(self.buoc)

        huong = huong_di_chuyen(self.ket_qua[self.buoc - 1], self.ket_qua[self.buoc])
        self.ds_nuoc_di.append(huong)
        
        log_str = f"Bước {self.buoc} | Hướng: {huong} ({giai_thich_huong(huong)})"
        
        if "values_g" in self.thong_tin_phu and "values_h" in self.thong_tin_phu and "values_f" in self.thong_tin_phu:
            if self.buoc < len(self.ket_qua):
                g_val = self.thong_tin_phu["values_g"][self.buoc]
                h_val = self.thong_tin_phu["values_h"][self.buoc]
                f_val = self.thong_tin_phu["values_f"][self.buoc]
                log_str += f" | g(n): {g_val} | h(n): {h_val} | f(n): {f_val}"
        else:
            if "cost" in self.thong_tin_phu and "values" in self.thong_tin_phu:
                if self.buoc < len(self.thong_tin_phu["values"]):
                    log_str += f" | Cost: {self.thong_tin_phu['values'][self.buoc]}"
                    
            if "depth" in self.thong_tin_phu and "values_depth" in self.thong_tin_phu:
                if self.buoc < len(self.thong_tin_phu["values_depth"]):
                    log_str += f" | Depth: {self.thong_tin_phu['values_depth'][self.buoc]}"
            
            if "heuristic" in self.thong_tin_phu and "values" in self.thong_tin_phu:
                 if self.buoc < len(self.thong_tin_phu["values"]):
                    log_str += f" | h(n): {self.thong_tin_phu['values'][self.buoc]}"

        self.txt_log.config(state="normal")
        self.txt_log.insert(tk.END, log_str + "\n")
        self.txt_log.insert(tk.END, doi_trang_thai_thanh_chuoi(self.ket_qua[self.buoc]))
        self.txt_log.insert(tk.END, "-"*60 + "\n")
        
        if self.buoc == len(self.ket_qua) - 1:
            self.ghi_lai_chuoi_nuoc_di()
            
        self.txt_log.see(tk.END)
        self.txt_log.config(state="disabled")

    def ghi_lai_chuoi_nuoc_di(self):
        self.txt_log.insert(tk.END, "\nChuỗi nước đi hoàn chỉnh:\n")
        if len(self.ds_nuoc_di) == 0:
            self.txt_log.insert(tk.END, "Không có nước đi (Đã ở đích)\n")
        else:
            self.txt_log.insert(tk.END, " -> ".join(self.ds_nuoc_di) + "\n")

    def chay_thuat_toan(self, ten, ham):
        if self.dang_tim_kiem: return
        
        self.dang_chay = False
        self.buoc = 0
        self.ten_thuat_toan = ten
        self.lbl_result.config(text=f"Đang tìm kiếm bằng {ten}... Vui lòng đợi.", fg="#d97706")
        self.xoa_log()
        
        self.dang_tim_kiem = True
        self.toggle_buttons(tk.DISABLED)
        
        thread = threading.Thread(target=self._thread_thuat_toan, args=(ten, ham))
        thread.start()

    def _thread_thuat_toan(self, ten, ham):
        try:
            ket_qua_raw = ham(self.bang, self.dich)
        except Exception as e:
            ket_qua_raw = (None, 0, f"Lỗi: {str(e)}")
            
        self.ket_qua_tam = ket_qua_raw
        self.ten_tam = ten
        self.root.event_generate("<<SearchDone>>", when="tail")

    def _xu_ly_ket_qua_sau_khi_chay(self, event=None):
        ten = self.ten_tam
        ket_qua_raw = self.ket_qua_tam

        self.dang_tim_kiem = False
        self.toggle_buttons(tk.NORMAL)

        if len(ket_qua_raw) == 4:
            self.ket_qua, so_node, trang_thai, self.thong_tin_phu = ket_qua_raw
        else:
             self.ket_qua, so_node, trang_thai = ket_qua_raw
             self.thong_tin_phu = {}

        if self.ket_qua is None or len(self.ket_qua) == 0:
            self.ket_qua = []
            self.lbl_result.config(text=f"{ten} | {trang_thai} | Node duyệt = {so_node}", fg="#b91c1c")
        else:
            so_buoc = len(self.ket_qua) - 1
            res_str = f"{ten} | Số bước = {so_buoc} | Node duyệt = {so_node}"
            
            if ten == "A*" or ten == "IDA*":
                if "cost" in self.thong_tin_phu:
                    res_str = f"{ten} | Số bước = {so_buoc} | Node duyệt = {so_node} | Tổng cost f(n) = {self.thong_tin_phu['cost']}"
                if ten == "IDA*" and "threshold" in self.thong_tin_phu:
                    res_str += f" | Threshold cuối = {self.thong_tin_phu['threshold']}"
                res_str += f" | {trang_thai}"
            else:
                if "cost" in self.thong_tin_phu:
                    res_str += f" | Tổng cost = {self.thong_tin_phu['cost']}"
                if "heuristic" in self.thong_tin_phu and "h_start" in self.thong_tin_phu:
                    res_str += f" | h(Start) = {self.thong_tin_phu['h_start']} | h(Goal) = 0"
                if "depth" in self.thong_tin_phu:
                    res_str += f" | Max Depth = {self.thong_tin_phu['depth']}"
                res_str += f" | {trang_thai}"
            
            self.lbl_result.config(text=res_str, fg="#047857")
            self.hien_bang(doi_list(self.ket_qua[0]))
            self.them_log_bat_dau()
            
            if ten == "IDA*" and "threshold_history" in self.thong_tin_phu:
                self.txt_log.config(state="normal")
                self.txt_log.insert(tk.END, "Các ngưỡng IDA* đã thử:\n")
                history_str = " -> ".join(map(str, self.thong_tin_phu["threshold_history"]))
                self.txt_log.insert(tk.END, history_str + "\n")
                self.txt_log.insert(tk.END, "-"*60 + "\n")
                self.txt_log.see(tk.END)
                self.txt_log.config(state="disabled")

    def hien_buoc(self):
        if not self.ket_qua: return
        self.hien_bang(doi_list(self.ket_qua[self.buoc]))

    def bam_truoc(self):
        if not self.ket_qua or self.dang_tim_kiem: return
        if self.buoc > 0:
            self.buoc -= 1
            self.hien_buoc()
        else:
            self.lbl_result.config(text="Đã ở trạng thái bắt đầu")

    def bam_tiep(self):
        if not self.ket_qua or self.dang_tim_kiem: return
        if self.buoc < len(self.ket_qua) - 1:
            self.buoc += 1
            self.hien_buoc()
            self.them_log_buoc_di()
        else:
            self.lbl_result.config(text="Đã tới trạng thái đích")

    def tu_dong_chay(self):
        if not self.dang_chay or not self.ket_qua:
            self.dang_chay = False
            return
            
        if self.buoc < len(self.ket_qua) - 1:
            self.buoc += 1
            self.hien_buoc()
            self.them_log_buoc_di()
            self.root.after(self.toc_do, self.tu_dong_chay)
        else:
            self.dang_chay = False

    def bam_tu_dong(self):
        if not self.ket_qua or self.dang_tim_kiem: return
        if self.dang_chay: return
        
        if self.buoc == len(self.ket_qua) - 1:
            self.buoc = 0
            self.xoa_log()
            self.hien_bang(doi_list(self.ket_qua[0]))
            self.them_log_bat_dau()
            
        self.dang_chay = True
        self.tu_dong_chay()

    def bam_dung(self):
        self.dang_chay = False

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()