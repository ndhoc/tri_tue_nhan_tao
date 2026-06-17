import random
import tkinter as tk
from tkinter import ttk
import threading
import math

# Import our modularized algorithms and helpers
from algorithms.common import (
    tim_so_0, doi_tuple, doi_list, dem_nghich_the, co_giai_duoc,
    sinh_ma_tran, tao_con, huong_di_chuyen, giai_thich_huong,
    doi_trang_thai_thanh_chuoi, manhattan_distance, dem_o_sai,
    dem_o_sai_khong_tinh_0, SearchCancelledException
)
from algorithms.bfs import bfs_phien_ban_1, bfs_phien_ban_2
from algorithms.dfs import dfs
from algorithms.ids import ids
from algorithms.ucs import ucs
from algorithms.greedy import greedy_search
from algorithms.astar import a_star
from algorithms.idastar import ida_star
from algorithms.hill_climbing import (
    local_search, simple_hill_climbing, steepest_ascent_hill_climbing,
    stochastic_hill_climbing, random_restart_hill_climbing
)
from algorithms.beam_search import local_beam_search
from algorithms.simulated_annealing import simulated_annealing, simulated_annealing_belief
from algorithms.and_or_search import and_or_graph_search
from algorithms.backtracking_search import backtracking_search
from algorithms.forward_checking import forward_checking_search

ds_thuat_toan = [
    ("BFS Version 1", bfs_phien_ban_1),
    ("BFS Version 2", bfs_phien_ban_2),
    ("DFS", dfs),
    ("IDS", ids),
    ("UCS", ucs),
    ("Greedy Search", greedy_search),
    ("A*", a_star),
    ("IDA*", ida_star),
    ("Local Search", local_search),
    ("Simple Hill Climbing", simple_hill_climbing),
    ("Steepest-ascent HC", steepest_ascent_hill_climbing),
    ("Stochastic HC", stochastic_hill_climbing),
    ("Random Restart HC", random_restart_hill_climbing),
    ("Local Beam Search", local_beam_search),
    ("Simulated Annealing", simulated_annealing),
    ("AND-OR Search", and_or_graph_search),
    ("Backtracking CSP", backtracking_search),
    ("Forward Checking", forward_checking_search)
]

def sinh_cac_trang_thai_tu_khuon(khuon, k, parity_must_be_even=True):
    flat_khuon = [khuon[i][j] for i in range(3) for j in range(3)]
    hidden_positions = [i for i, val in enumerate(flat_khuon) if val == '?']
    visible_values = [val for val in flat_khuon if val != '?']
    missing_values = [val for val in range(9) if val not in visible_values]
    
    states = []
    attempts = 0
    while len(states) < k and attempts < 5000:
        attempts += 1
        curr_missing = list(missing_values)
        random.shuffle(curr_missing)
        
        state_flat = list(flat_khuon)
        for idx, pos in enumerate(hidden_positions):
            state_flat[pos] = curr_missing[idx]
            
        state_grid = [state_flat[i*3:(i+1)*3] for i in range(3)]
        
        if co_giai_duoc(state_grid) == parity_must_be_even:
            state_tuple = doi_tuple(state_grid)
            if state_tuple not in states:
                states.append(state_tuple)
                
    if not states:
        # Fallback to a random solvable matrix
        for _ in range(k):
            states.append(doi_tuple(sinh_ma_tran()))
            
    while len(states) < k:
        states.append(states[0])
    return states


class SimulationWindow(tk.Toplevel):
    def __init__(self, parent, algo_name, algo_func, starts, goals, is_belief, k, toc_do, sa_params=None, extra_params=None):
        super().__init__(parent)
        self.title(f"Mô Phỏng Thuật Toán: {algo_name}")
        self.geometry("1150x780")
        self.configure(bg="#f8fafc")
        
        self.parent = parent
        self.algo_name = algo_name
        self.algo_func = algo_func
        self.starts = starts
        self.goals = goals
        self.is_belief = is_belief
        self.k = k
        self.toc_do = toc_do
        self.sa_params = sa_params or {"T0": 100.0, "Tmin": 0.05, "alpha": 0.995, "max_steps": 2000}
        self.extra_params = extra_params or {"max_restart": 50, "k_beam": 5}
        
        self.path = []
        self.actions = []
        self.trang_thai = "Đang tìm kiếm..."
        self.current_step = 0
        self.dang_chay = False
        self.dang_tim_kiem = True
        self.extra_info = {}
        self.is_csp_algo = algo_name in ["Backtracking CSP", "Forward Checking"]
        
        self.is_destroyed = False
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.setup_ui()
        self.start_search_thread()
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e3a8a", pady=12)
        header.pack(fill=tk.X)
        
        mode_text = f"Môi trường không nhìn thấy (Belief State) | Kích thước Belief k = {self.k}" if self.is_belief else "Môi trường quan sát đầy đủ"
        tk.Label(header, text=f"MÔ PHỎNG: {self.algo_name.upper()}", font=("Segoe UI", 16, "bold"), fg="#ffffff", bg="#1e3a8a").pack()
        tk.Label(header, text=mode_text, font=("Segoe UI", 10), fg="#93c5fd", bg="#1e3a8a").pack()
        
        # Main body
        body = tk.Frame(self, bg="#f8fafc")
        body.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left frame: Boards
        self.left_frame = tk.Frame(body, bg="#ffffff", bd=1, relief="solid", padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Goal display at the top of left frame
        goals_container = tk.Frame(self.left_frame, bg="#ffffff", pady=5)
        goals_container.pack(fill=tk.X, pady=(0, 10))
        goal_lbl_text = "Trạng thái Đích (Goal states):" if self.is_belief else "Trạng thái Đích (Goal state):"
        tk.Label(goals_container, text=goal_lbl_text, font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#047857").pack(anchor=tk.W)
        
        goals_grid = tk.Frame(goals_container, bg="#ffffff")
        goals_grid.pack(anchor=tk.W, pady=2)
        
        num_goals = len(self.goals)
        for g_idx, goal in enumerate(self.goals):
            gf = tk.Frame(goals_grid, bg="#ffffff", bd=1, relief="solid", padx=2, pady=2)
            gf.pack(side=tk.LEFT, padx=5)
            tk.Label(gf, text=f"Goal {g_idx+1}" if num_goals > 1 else "Goal", font=("Segoe UI", 8, "bold"), bg="#ffffff", fg="#047857").pack()
            
            g_board = tk.Frame(gf, bg="#cbd5e1")
            g_board.pack()
            for r in range(3):
                for c in range(3):
                    val = goal[r][c]
                    text = "?" if val == '?' else (str(val) if val != 0 else "")
                    bg = "#cbd5e1" if (val == 0 or val == '?') else "#ffffff"
                    lbl = tk.Label(g_board, text=text, width=3, height=1, font=("Segoe UI", 10, "bold"), bg=bg)
                    lbl.grid(row=r, column=c, padx=1, pady=1)
                    
        ttk.Separator(self.left_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        
        # Current Board States display
        current_lbl_text = "Trạng thái Hiện tại (Current belief states):" if self.is_belief else "Trạng thái Hiện tại (Current state):"
        tk.Label(self.left_frame, text=current_lbl_text, font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e3a8a").pack(anchor=tk.W)
        self.board_frame = tk.Frame(self.left_frame, bg="#ffffff")
        self.board_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Right frame: Controls & Stats & Log
        right_frame = tk.Frame(body, bg="#ffffff", bd=1, relief="solid", width=360, padx=15, pady=15)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Status Label
        self.lbl_status = tk.Label(right_frame, text="Đang khởi tạo...", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#d97706", wraplength=330, justify="left")
        self.lbl_status.pack(anchor=tk.W, pady=(0, 10))
        
        # Stats Grid
        stats_frame = tk.LabelFrame(right_frame, text="Thông số mô phỏng", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1e3a8a", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=5)
        
        stats_frame.columnconfigure(1, weight=1)
        
        tk.Label(stats_frame, text="Bước hiện tại:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=2)
        self.lbl_step = tk.Label(stats_frame, text="-", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#2563eb")
        self.lbl_step.grid(row=0, column=1, sticky="w", padx=10, pady=2)
        
        tk.Label(stats_frame, text="Hành động vừa rồi:", font=("Segoe UI", 9), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=2)
        self.lbl_action = tk.Label(stats_frame, text="-", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#10b981")
        self.lbl_action.grid(row=1, column=1, sticky="w", padx=10, pady=2)
        
        self.lbl_cost_name = tk.Label(stats_frame, text="Giá trị:", font=("Segoe UI", 9), bg="#ffffff")
        self.lbl_cost_name.grid(row=2, column=0, sticky="w", pady=2)
        self.lbl_h = tk.Label(stats_frame, text="-", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#b91c1c")
        self.lbl_h.grid(row=2, column=1, sticky="w", padx=10, pady=2)
        
        tk.Label(stats_frame, text="Nhiệt độ T:", font=("Segoe UI", 9), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=2)
        self.lbl_temp = tk.Label(stats_frame, text="-", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#f97316")
        self.lbl_temp.grid(row=3, column=1, sticky="w", padx=10, pady=2)
        
        # Playback Controls
        ctrls = tk.Frame(right_frame, bg="#ffffff")
        ctrls.pack(fill=tk.X, pady=10)
        
        btn_row = tk.Frame(ctrls, bg="#ffffff")
        btn_row.pack(fill=tk.X, pady=2)
        
        self.btn_truoc = tk.Button(btn_row, text="Bước trước", font=("Segoe UI", 9), bg="#e2e8f0", fg="#1e293b", relief="flat", command=self.bam_truoc)
        self.btn_truoc.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        
        self.btn_tiep = tk.Button(btn_row, text="Bước sau", font=("Segoe UI", 9), bg="#e2e8f0", fg="#1e293b", relief="flat", command=self.bam_tiep)
        self.btn_tiep.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))
        
        self.btn_auto = tk.Button(ctrls, text="Tự động chạy", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", command=self.bam_tu_dong)
        self.btn_auto.pack(fill=tk.X, pady=4)
        
        btn_row2 = tk.Frame(ctrls, bg="#ffffff")
        btn_row2.pack(fill=tk.X, pady=2)
        
        self.btn_dung = tk.Button(btn_row2, text="Dừng", font=("Segoe UI", 9), bg="#fca5a5", fg="#991b1b", relief="flat", command=self.bam_dung)
        self.btn_dung.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        
        btn_close = tk.Button(btn_row2, text="Đóng", font=("Segoe UI", 9), bg="#cbd5e1", fg="#334155", relief="flat", command=self.destroy)
        btn_close.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(2, 0))
        
        tk.Label(ctrls, text="Tốc độ chạy (ms):", font=("Segoe UI", 9), bg="#ffffff").pack(anchor=tk.W, pady=(5, 0))
        self.scale_speed = ttk.Scale(ctrls, from_=50, to=2000, orient="horizontal", command=self.doi_toc_do)
        self.scale_speed.set(self.toc_do)
        self.scale_speed.pack(fill=tk.X, pady=5)
        

        
        # Log Text Box
        tk.Label(right_frame, text="Log hoạt động", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#475569").pack(anchor=tk.W, pady=(5, 2))
        log_scroll = ttk.Scrollbar(right_frame, orient="vertical")
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log = tk.Text(right_frame, height=10, font=("Consolas", 9), bg="#f1f5f9", fg="#334155", wrap="none", yscrollcommand=log_scroll.set)
        self.txt_log.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.txt_log.yview)
        self.txt_log.config(state="disabled")
        
        self.setup_boards()
        
    def setup_boards(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()
            
        self.board_cells = []
        num_boards = self.k if self.is_belief else 1
        cols = 3 if num_boards <= 3 else 2
        
        for b_idx in range(num_boards):
            bf = tk.LabelFrame(self.board_frame, text=f"Trạng thái {b_idx + 1}" if num_boards > 1 else "Bàn cờ", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1e3a8a", padx=5, pady=5)
            r = b_idx // cols
            c = b_idx % cols
            bf.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
            
            cells = []
            for i in range(3):
                row_cells = []
                for j in range(3):
                    lbl = tk.Label(bf, text="", width=4, height=2, 
                                   font=("Segoe UI", 14, "bold"), bg="#f1f5f9", fg="#1e293b", relief="solid", bd=1)
                    lbl.grid(row=i, column=j, padx=2, pady=2)
                    row_cells.append(lbl)
                cells.append(row_cells)
            self.board_cells.append(cells)
            
    def doi_toc_do(self, value):
        self.toc_do = int(float(value))
        
    def start_search_thread(self):
        self.lbl_status.config(text="Đang tính toán nước đi... Vui lòng đợi.", fg="#d97706")
        self.btn_auto.config(state=tk.DISABLED)
        self.btn_truoc.config(state=tk.DISABLED)
        self.btn_tiep.config(state=tk.DISABLED)
        self.btn_dung.config(state=tk.DISABLED)
        
        thread_name = f"SearchThread_{id(self)}"
        self.search_thread = threading.Thread(target=self.run_algorithm, name=thread_name, daemon=True)
        self.search_thread.start()
        self.after(100, self.check_search_done)
        
    def on_close(self):
        self.is_destroyed = True
        thread_name = f"SearchThread_{id(self)}"
        from algorithms.common import cancelled_threads
        cancelled_threads.add(thread_name)
        self.destroy()
        
    def run_algorithm(self):
        try:
            if self.is_belief:
                if self.algo_name == "Simulated Annealing":
                    self.path, self.actions, self.so_node, self.trang_thai, self.extra_info = simulated_annealing_belief(
                        self.starts, self.goals,
                        T0=self.sa_params["T0"], Tmin=self.sa_params["Tmin"], alpha=self.sa_params["alpha"],
                        max_steps=self.sa_params["max_steps"]
                    )
                elif self.algo_name == "Local Beam Search":
                    res = self.algo_func(tuple(self.starts), self.goals, k=self.extra_params.get("k_beam", 5))
                elif self.algo_name == "Random Restart HC":
                    res = self.algo_func(tuple(self.starts), self.goals, max_restart=self.extra_params.get("max_restart", 50))
                elif self.is_csp_algo:
                    res = self.algo_func(tuple(self.starts), self.goals)
                else:
                    # Run generic search algorithm in belief space
                    res = self.algo_func(tuple(self.starts), self.goals)
                
                if self.algo_name != "Simulated Annealing":
                    if len(res) == 4:
                        self.path, self.so_node, self.trang_thai, self.extra_info = res
                    else:
                        self.path, self.so_node, self.trang_thai = res
                        self.extra_info = {}
                    
                    # Compute actions taken in belief state transitions
                    self.actions = []
                    if self.path:
                        for idx in range(len(self.path) - 1):
                            self.actions.append(huong_di_chuyen(self.path[idx], self.path[idx+1]))
            else:
                if self.algo_name == "Simulated Annealing":
                    self.path, self.so_node, self.trang_thai, self.extra_info = simulated_annealing(
                        self.starts[0], self.goals[0],
                        T0=self.sa_params["T0"], Tmin=self.sa_params["Tmin"], alpha=self.sa_params["alpha"],
                        max_steps=self.sa_params["max_steps"]
                    )
                elif self.algo_name == "Local Beam Search":
                    res = self.algo_func(self.starts[0], self.goals[0], k=self.extra_params.get("k_beam", 5))
                elif self.algo_name == "Random Restart HC":
                    res = self.algo_func(self.starts[0], self.goals[0], max_restart=self.extra_params.get("max_restart", 50))
                elif self.is_csp_algo:
                    res = self.algo_func(self.starts[0], self.goals[0])
                else:
                    res = self.algo_func(self.starts[0], self.goals[0])
                
                if self.algo_name != "Simulated Annealing":
                    if len(res) == 4:
                        self.path, self.so_node, self.trang_thai, self.extra_info = res
                    else:
                        self.path, self.so_node, self.trang_thai = res
                        self.extra_info = {}
                    self.actions = []
        except SearchCancelledException:
            # Thread was cancelled due to window closure, do nothing
            pass
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.path = None
            self.trang_thai = f"Lỗi: {str(e)}"
            self.so_node = 0
            self.extra_info = {}
            
    def check_search_done(self):
        if getattr(self, "is_destroyed", False):
            return
        try:
            if not self.winfo_exists():
                return
        except tk.TclError:
            return

        if self.search_thread.is_alive():
            try:
                self.after(100, self.check_search_done)
            except tk.TclError:
                pass
        else:
            self.dang_tim_kiem = False
            self.btn_auto.config(state=tk.NORMAL)
            self.btn_truoc.config(state=tk.NORMAL)
            self.btn_tiep.config(state=tk.NORMAL)
            self.btn_dung.config(state=tk.NORMAL)
            
            if self.path is None or len(self.path) == 0:
                self.lbl_status.config(text=f"Thất bại: {self.trang_thai}", fg="#ef4444")
            else:
                self.lbl_status.config(text=f"Đã chạy xong! Kết quả: {self.trang_thai}", fg="#10b981")
                self.current_step = 0
                
                # Update label name based on algorithm
                if self.algo_name in ["BFS Version 1", "BFS Version 2", "DFS", "IDS", "AND-OR Search", "Backtracking CSP", "Forward Checking"]:
                    self.lbl_cost_name.config(text="Cost path:")
                elif self.algo_name == "UCS":
                    self.lbl_cost_name.config(text="g(B):" if self.is_belief else "g(n):")
                elif self.algo_name in ["A*", "IDA*"]:
                    self.lbl_cost_name.config(text="f(B):" if self.is_belief else "f(n):")
                elif self.algo_name == "Greedy Search":
                    self.lbl_cost_name.config(text="h(B):" if self.is_belief else "h(n):")
                else: # Local Search, HC variants, Beam Search, Simulated Annealing
                    self.lbl_cost_name.config(text="h(B):" if self.is_belief else "h(n):")
                    
                self.hien_trang_thai_buoc(0)
                self.ghi_log_tat_ca()
                
    def hien_trang_thai_buoc(self, step_idx):
        if not self.path:
            return
            
        num_boards = self.k if self.is_belief else 1
        
        if self.is_belief:
            belief = self.path[step_idx]
            for b_idx in range(num_boards):
                if b_idx < len(belief):
                    self.hien_bang_board(b_idx, belief[b_idx])
        else:
            self.hien_bang_board(0, self.path[step_idx])
            
        self.lbl_step.config(text=f"{step_idx} / {len(self.path) - 1}")
        
        if self.algo_name in ["A*", "IDA*"]:
            history_h = self.extra_info.get("values_f", self.extra_info.get("values", []))
        elif self.algo_name == "UCS":
            history_h = self.extra_info.get("values", [])
        else:
            history_h = self.extra_info.get("history_h", self.extra_info.get("values", []))
            
        history_T = self.extra_info.get("history_T", [])
        
        if step_idx < len(history_h):
            self.lbl_h.config(text=f"{history_h[step_idx]}")
        else:
            self.lbl_h.config(text="-")
            
        if history_T and step_idx < len(history_T):
            self.lbl_temp.config(text=f"{history_T[step_idx]:.3f}")
        else:
            self.lbl_temp.config(text="-")
            
        assignment_log = self.extra_info.get("assignment_log", [])
        if step_idx > 0:
            if self.is_csp_algo and step_idx - 1 < len(assignment_log):
                var, val = assignment_log[step_idx - 1]
                self.lbl_action.config(text=f"Gan x_{var+1} = {val}")
            elif self.is_belief and step_idx - 1 < len(self.actions):
                act = self.actions[step_idx - 1]
                self.lbl_action.config(text=f"{act} ({giai_thich_huong(act)})")
            elif not self.is_belief:
                act = huong_di_chuyen(self.path[step_idx - 1], self.path[step_idx])
                self.lbl_action.config(text=f"{act} ({giai_thich_huong(act)})")
        else:
            self.lbl_action.config(text="START" if not self.is_csp_algo else "Assignment = []")
            
    def hien_bang_board(self, b_idx, state):
        cells = self.board_cells[b_idx]
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val == -1:
                    # Ô chưa được gán (CSP)
                    cells[i][j].config(text="?", bg="#fef3c7", fg="#92400e")
                elif val == 0:
                    cells[i][j].config(text="", bg="#e2e8f0")
                elif val == '?':
                    cells[i][j].config(text="?", bg="#cbd5e1")
                else:
                    cells[i][j].config(text=str(val), bg="#ffffff", fg="#1e293b")
                    

                
    def bam_truoc(self):
        if not self.path or self.dang_tim_kiem: return
        if self.current_step > 0:
            self.current_step -= 1
            self.hien_trang_thai_buoc(self.current_step)
            
    def bam_tiep(self):
        if not self.path or self.dang_tim_kiem: return
        if self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.hien_trang_thai_buoc(self.current_step)
            
    def tu_dong_chay(self):
        if not self.dang_chay or not self.path:
            self.dang_chay = False
            return
            
        if self.current_step < len(self.path) - 1:
            self.current_step += 1
            self.hien_trang_thai_buoc(self.current_step)
            self.after(self.toc_do, self.tu_dong_chay)
        else:
            self.dang_chay = False
            
    def bam_tu_dong(self):
        if not self.path or self.dang_tim_kiem: return
        if self.dang_chay: return
        
        if self.current_step == len(self.path) - 1:
            self.current_step = 0
            self.hien_trang_thai_buoc(0)
            
        self.dang_chay = True
        self.tu_dong_chay()
        
    def bam_dung(self):
        self.dang_chay = False
        
    def ghi_log_tat_ca(self):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", tk.END)
        
        self.txt_log.insert(tk.END, "LOG CHI TIET QUA TRINH\n")
        self.txt_log.insert(tk.END, f"Thuat toan: {self.algo_name}\n")
        self.txt_log.insert(tk.END, f"Moi truong: {'Khong nhin thay' if self.is_belief else 'Quan sat day du'}\n")
        self.txt_log.insert(tk.END, f"So buoc: {len(self.path) - 1}\n")
        self.txt_log.insert(tk.END, "-"*40 + "\n")
        
        history_h = self.extra_info.get("history_h", self.extra_info.get("values", []))
        history_T = self.extra_info.get("history_T", [])
        assignment_log = self.extra_info.get("assignment_log", [])
        
        for idx in range(len(self.path)):
            log_str = f"Buoc {idx}"
            if idx > 0:
                if self.is_csp_algo and idx - 1 < len(assignment_log):
                    var, val = assignment_log[idx - 1]
                    log_str += f" | Gan x_{var+1} = {val}"
                elif self.is_belief and idx - 1 < len(self.actions):
                    act = self.actions[idx - 1]
                    log_str += f" | {act} ({giai_thich_huong(act)})"
                elif not self.is_belief:
                    act = huong_di_chuyen(self.path[idx-1], self.path[idx])
                    log_str += f" | {act} ({giai_thich_huong(act)})"
            else:
                log_str += " | START" if not self.is_csp_algo else " | Assignment = []"
                
            if idx < len(history_h):
                log_str += f" | h: {history_h[idx]}"
            if history_T and idx < len(history_T):
                log_str += f" | T: {history_T[idx]:.2f}"
                
            self.txt_log.insert(tk.END, log_str + "\n")
            
            if self.is_csp_algo:
                # Hien thi bang 3x3 voi ? cho o chua gan
                state = self.path[idx]
                for r in range(3):
                    row_str = ""
                    for c in range(3):
                        v = state[r][c]
                        if v == -1:
                            row_str += "? "
                        elif v == 0:
                            row_str += "_ "
                        else:
                            row_str += str(v) + " "
                    self.txt_log.insert(tk.END, row_str + "\n")
            elif self.is_belief:
                belief = self.path[idx]
                for b_idx, st in enumerate(belief):
                    self.txt_log.insert(tk.END, f"  * Ban co {b_idx+1}:\n")
                    self.txt_log.insert(tk.END, self.indent_text(doi_trang_thai_thanh_chuoi(st), "    "))
            else:
                self.txt_log.insert(tk.END, doi_trang_thai_thanh_chuoi(self.path[idx]))
                
            self.txt_log.insert(tk.END, "-"*40 + "\n")
            
        if self.is_csp_algo and assignment_log:
            self.txt_log.insert(tk.END, "\nThu tu gan bien:\n")
            assigns = [f"x_{var+1}={val}" for var, val in assignment_log]
            self.txt_log.insert(tk.END, " -> ".join(assigns) + "\n")
        elif self.is_belief and self.actions:
            self.txt_log.insert(tk.END, "\nChuoi nuoc di hoan chinh:\n")
            self.txt_log.insert(tk.END, " -> ".join(self.actions) + "\n")
        elif not self.is_belief and len(self.path) > 1:
            self.txt_log.insert(tk.END, "\nChuoi nuoc di hoan chinh:\n")
            acts = []
            for i in range(1, len(self.path)):
                acts.append(huong_di_chuyen(self.path[i-1], self.path[i]))
            self.txt_log.insert(tk.END, " -> ".join(acts) + "\n")
            
        self.txt_log.config(state="disabled")
        
    def indent_text(self, text, indent):
        return "".join(indent + line + "\n" for line in text.strip().split("\n"))


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Visualizer")
        self.root.geometry("1150x750")
        self.root.configure(bg="#f1f5f9")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("TFrame", background="#f1f5f9")
        self.style.configure("TLabel", background="#f1f5f9", font=("Segoe UI", 11))

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

        self.start_template = doi_list(self.bang)
        self.goal_template = doi_list(self.dich)
        
        self.setup_ui()
        self.hien_bang_start(self.start_template)
        self.hien_bang_goal(self.goal_template)

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#f1f5f9")
        header_frame.pack(fill=tk.X, pady=8)
        
        tk.Label(header_frame, text="8-Puzzle Visualizer", font=("Segoe UI", 16, "bold"), fg="#1e3a8a", bg="#f1f5f9").pack()
        tk.Label(header_frame, text="Mô phỏng tìm kiếm trong môi trường biết hoặc không biết trạng thái", font=("Segoe UI", 11), fg="#4b5563", bg="#f1f5f9").pack()

        main_frame = tk.Frame(self.root, bg="#f1f5f9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        left_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid", padx=15, pady=15)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Start and Goal side-by-side
        boards_container = tk.Frame(left_frame, bg="#ffffff")
        boards_container.pack(pady=10)
        
        # Start Board
        start_outer = tk.Frame(boards_container, bg="#ffffff")
        start_outer.pack(side=tk.LEFT, padx=20)
        tk.Label(start_outer, text="TRẠNG THÁI BẮT ĐẦU", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e3a8a").pack(pady=5)
        self.start_board_frame = tk.Frame(start_outer, bg="#94a3b8", bd=4, relief="ridge")
        self.start_board_frame.pack()
        
        self.cells_start = []
        for i in range(3):
            row_cells = []
            for j in range(3):
                lbl = tk.Label(self.start_board_frame, text="", width=4, height=2, 
                               font=("Segoe UI", 22, "bold"), bg="#ffffff", fg="#1e293b", relief="raised", bd=3)
                lbl.grid(row=i, column=j, padx=3, pady=3)
                row_cells.append(lbl)
            self.cells_start.append(row_cells)

        # Goal Board
        goal_outer = tk.Frame(boards_container, bg="#ffffff")
        goal_outer.pack(side=tk.RIGHT, padx=20)
        tk.Label(goal_outer, text="TRẠNG THÁI ĐÍCH", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#047857").pack(pady=5)
        self.goal_board_frame = tk.Frame(goal_outer, bg="#94a3b8", bd=4, relief="ridge")
        self.goal_board_frame.pack()
        
        self.cells_goal = []
        for i in range(3):
            row_cells = []
            for j in range(3):
                lbl = tk.Label(self.goal_board_frame, text="", width=4, height=2, 
                               font=("Segoe UI", 22, "bold"), bg="#ffffff", fg="#1e293b", relief="raised", bd=3)
                lbl.grid(row=i, column=j, padx=3, pady=3)
                row_cells.append(lbl)
            self.cells_goal.append(row_cells)

        self.lbl_main_info = tk.Label(left_frame, text="Chọn thuật toán ở bảng bên phải để mở cửa sổ trực quan chi tiết.", font=("Segoe UI", 11, "italic"), fg="#475569", bg="#ffffff", justify="center")
        self.lbl_main_info.pack(pady=15)

        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=1, relief="solid", width=360)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        canvas = tk.Canvas(right_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        control_inner = tk.Frame(canvas, bg="#ffffff", padx=10, pady=10)
        
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
        
        # Environment Settings
        env_frame = tk.LabelFrame(control_inner, text="Chế độ Môi trường", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1e40af", padx=8, pady=5)
        env_frame.pack(fill=tk.X, pady=4)
        
        self.var_mode = tk.StringVar(value="normal")
        
        modes = [
            ("Quan sát đầy đủ", "normal"),
            ("Khuyết Start", "khuyet_start"),
            ("Khuyết Goal", "khuyet_goal"),
            ("Khuyết 1 phần", "khuyet_mot_phan")
        ]
        
        for idx, (text, val) in enumerate(modes):
            r = idx // 2
            c = idx % 2
            tk.Radiobutton(env_frame, text=text, variable=self.var_mode, value=val, font=("Segoe UI", 9), bg="#ffffff", activebackground="#ffffff", command=self.cap_nhat_giao_dien_che_do).grid(row=r, column=c, sticky="w", padx=2, pady=1)
        env_frame.columnconfigure(0, weight=1)
        env_frame.columnconfigure(1, weight=1)
            
        param_frame = tk.Frame(control_inner, bg="#ffffff")
        param_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(param_frame, text="k (Belief):", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=2)
        self.entry_k = ttk.Entry(param_frame, width=5)
        self.entry_k.insert(0, "2")
        self.entry_k.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        
        tk.Label(param_frame, text="Số ô ẩn:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=2, sticky="w", padx=(10, 0), pady=2)
        self.entry_hide_count = ttk.Entry(param_frame, width=5)
        self.entry_hide_count.insert(0, "3")
        self.entry_hide_count.grid(row=0, column=3, sticky="w", padx=2, pady=2)
        
        tk.Label(param_frame, text="Restart:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=4, sticky="w", padx=(10, 0), pady=2)
        self.entry_restart = ttk.Entry(param_frame, width=5)
        self.entry_restart.insert(0, "50")
        self.entry_restart.grid(row=0, column=5, sticky="w", padx=2, pady=2)
        
        # SA parameters
        sa_param_frame = tk.LabelFrame(control_inner, text="Tham số Luyện Thép", font=("Segoe UI", 10, "bold"), bg="#ffffff", fg="#1e40af", padx=8, pady=5)
        sa_param_frame.pack(fill=tk.X, pady=4)
        
        tk.Label(sa_param_frame, text="T0:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=1)
        self.entry_t0 = ttk.Entry(sa_param_frame, width=5)
        self.entry_t0.insert(0, "100.0")
        self.entry_t0.grid(row=0, column=1, sticky="w", padx=2, pady=1)
        
        tk.Label(sa_param_frame, text="Tmin:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=2, sticky="w", padx=(5, 0), pady=1)
        self.entry_tmin = ttk.Entry(sa_param_frame, width=5)
        self.entry_tmin.insert(0, "0.05")
        self.entry_tmin.grid(row=0, column=3, sticky="w", padx=2, pady=1)
        
        tk.Label(sa_param_frame, text="Alpha:", font=("Segoe UI", 9), bg="#ffffff").grid(row=0, column=4, sticky="w", padx=(5, 0), pady=1)
        self.entry_alpha = ttk.Entry(sa_param_frame, width=6)
        self.entry_alpha.insert(0, "0.995")
        self.entry_alpha.grid(row=0, column=5, sticky="w", padx=2, pady=1)
 
        ttk.Separator(control_inner, orient='horizontal').pack(fill=tk.X, pady=5)
 
        tk.Label(control_inner, text="Chọn Thuật Toán", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#1e40af").pack(anchor=tk.W, pady=(0, 3))
        
        algo_frame = tk.Frame(control_inner, bg="#ffffff")
        algo_frame.pack(fill=tk.X, pady=1)
        
        self.algo_buttons = []
        for idx, (ten, ham) in enumerate(ds_thuat_toan):
            btn = tk.Button(algo_frame, text=ten, font=("Segoe UI", 9), bg="#e2e8f0", fg="#1e293b", relief="flat",
                            command=lambda t=ten, h=ham: self.bam_chay_thuat_toan(t, h))
            row = idx // 2
            col = idx % 2
            btn.grid(row=row, column=col, sticky="ew", padx=2, pady=1)
            self.algo_buttons.append(btn)
            
        algo_frame.columnconfigure(0, weight=1)
        algo_frame.columnconfigure(1, weight=1)

    def hien_bang_start(self, a):
        for i in range(3):
            for j in range(3):
                val = a[i][j]
                if val == 0:
                    self.cells_start[i][j].config(text="", bg="#cbd5e1")
                elif val == '?':
                    self.cells_start[i][j].config(text="?", bg="#94a3b8")
                else:
                    self.cells_start[i][j].config(text=str(val), bg="#ffffff")

    def hien_bang_goal(self, a):
        for i in range(3):
            for j in range(3):
                val = a[i][j]
                if val == 0:
                    self.cells_goal[i][j].config(text="", bg="#cbd5e1")
                elif val == '?':
                    self.cells_goal[i][j].config(text="?", bg="#94a3b8")
                else:
                    self.cells_goal[i][j].config(text=str(val), bg="#ffffff")

    def bam_sinh(self):
        self.bang = sinh_ma_tran()
        self.cap_nhat_giao_dien_che_do()
        self.lbl_main_info.config(text="Đã sinh trạng thái bắt đầu ngẫu nhiên mới.", fg="#047857")

    def bam_nhap_ma_tran(self):
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
                self.bang = vals
                self.cap_nhat_giao_dien_che_do()
                self.lbl_main_info.config(text="Đã nhập trạng thái bắt đầu mới.", fg="#047857")
                dialog.destroy()
            except ValueError:
                lbl_err.config(text="Vui lòng nhập số nguyên!")
        
        tk.Button(dialog, text="Xác nhận", font=("Segoe UI", 10, "bold"), bg="#10b981", fg="white", relief="flat", command=xac_nhan).pack(pady=5)

    def cap_nhat_giao_dien_che_do(self):
        mode = self.var_mode.get()
        self.start_template = doi_list(self.bang)
        self.goal_template = doi_list(self.dich)
        
        if mode == "khuyet_start":
            self.start_template = [['?' for _ in range(3)] for _ in range(3)]
        elif mode == "khuyet_goal":
            self.goal_template = [['?' for _ in range(3)] for _ in range(3)]
        elif mode == "khuyet_mot_phan":
            try:
                num_hide = int(self.entry_hide_count.get().strip())
            except ValueError:
                num_hide = 3
            num_hide = max(0, min(8, num_hide))
            
            # Hide non-zero random positions in start
            flat_start = [(r, c) for r in range(3) for c in range(3) if self.bang[r][c] != 0]
            for r, c in random.sample(flat_start, min(num_hide, len(flat_start))):
                self.start_template[r][c] = '?'
                
            # Hide non-zero random positions in goal
            flat_goal = [(r, c) for r in range(3) for c in range(3) if self.dich[r][c] != 0]
            for r, c in random.sample(flat_goal, min(num_hide, len(flat_goal))):
                self.goal_template[r][c] = '?'
                
        self.hien_bang_start(self.start_template)
        self.hien_bang_goal(self.goal_template)

    def bam_chay_thuat_toan(self, ten, ham):
        mode = self.var_mode.get()
        is_belief = (mode != "normal")
        
        try:
            k_val = int(self.entry_k.get().strip())
        except ValueError:
            k_val = 2
        k_val = max(1, k_val)
        
        try:
            restart_val = int(self.entry_restart.get().strip())
        except ValueError:
            restart_val = 50
        restart_val = max(1, restart_val)
        
        # No forced switch - all algorithms can run on belief state!
        self.lbl_main_info.config(text=f"Khởi động mô phỏng cho thuật toán {ten}...", fg="#10b981")
            
        # Generate start and goal states matching the templates
        if mode == "normal":
            starts = [doi_tuple(self.bang)]
            goals = [doi_tuple(self.dich)]
            is_belief = False
            k_val = 1
        elif mode == "khuyet_start":
            starts = sinh_cac_trang_thai_tu_khuon(self.start_template, k_val, parity_must_be_even=True)
            goals = [doi_tuple(self.dich)]
        elif mode == "khuyet_goal":
            starts = sinh_cac_trang_thai_tu_khuon(self.start_template, k_val, parity_must_be_even=True)
            goals = sinh_cac_trang_thai_tu_khuon(self.goal_template, k_val, parity_must_be_even=True)
        else: # khuyet_mot_phan
            starts = sinh_cac_trang_thai_tu_khuon(self.start_template, k_val, parity_must_be_even=True)
            goals = sinh_cac_trang_thai_tu_khuon(self.goal_template, k_val, parity_must_be_even=True)
            
        # Extract SA parameters
        try:
            t0_val = float(self.entry_t0.get().strip())
            tmin_val = float(self.entry_tmin.get().strip())
            alpha_val = float(self.entry_alpha.get().strip())
        except ValueError:
            t0_val = 100.0
            tmin_val = 0.05
            alpha_val = 0.995
            
        sa_params = {
            "T0": t0_val,
            "Tmin": tmin_val,
            "alpha": alpha_val,
            "max_steps": 2000
        }
        
        # Open simulation window
        sim_win = SimulationWindow(self.root, ten, ham, starts, goals, is_belief, k_val, toc_do=500, sa_params=sa_params, extra_params={"max_restart": restart_val, "k_beam": k_val})
        sim_win.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()