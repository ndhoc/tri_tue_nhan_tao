import random
import tkinter as tk
from queue import Queue

def rule(x, y):
    moves = []

    if (x == 0 and y == 0):
        moves = [(0, 1), (1, 0)]
    elif (x == 0 and y == 1):
        moves = [(0, 0), (0, 2), (1, 1)]
    elif (x == 0 and y == 2):
        moves = [(0, 1), (1, 2)]
    elif (x == 1 and y == 0):
        moves = [(0, 0), (1, 1), (2, 0)]
    elif (x == 1 and y == 1):
        moves = [(0, 1), (1, 0), (1, 2), (2, 1)]
    elif (x == 1 and y == 2):
        moves = [(0, 2), (1, 1), (2, 2)]
    elif (x == 2 and y == 0):
        moves = [(1, 0), (2, 1)]
    elif (x == 2 and y == 1):
        moves = [(1, 1), (2, 0), (2, 2)]
    else:
        moves = [(2, 1), (1, 2)]

    return moves

def tim_so_0(a):
    for i in range(3):
        for j in range(3):
            if (a[i][j] == 0):
                return i, j

def doi_tuple(a):
    b = []
    for i in range(3):
        hang = []
        for j in range(3):
            hang.append(a[i][j])
        b.append(tuple(hang))
    return tuple(b)


def doi_list(a):
    b = []
    for i in range(3):
        hang = []
        for j in range(3):
            hang.append(a[i][j])
        b.append(hang)
    return b


def dem_nghich_the(a):
    b = []
    for i in range(3):
        for j in range(3):
            if (a[i][j] != 0):
                b.append(a[i][j])
    dem = 0
    for i in range(len(b)):
        for j in range(i + 1, len(b)):
            if (b[i] > b[j]):
                dem = dem + 1
    return dem

def co_giai_duoc(a):
    if (dem_nghich_the(a) % 2 == 0):
        return True
    return False


def sinh_ma_tran():
    so = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while (True):
        random.shuffle(so)
        a = []; k = 0
        for i in range(3):
            hang = []
            for j in range(3):
                hang.append(so[k])
                k += 1
            a.append(hang)
        if (co_giai_duoc(a) == True):
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
    if (huong == "U"): return "Up"
    elif (huong == "D"): return "Down"
    elif (huong == "L"): return "Left"
    elif (huong == "R"): return "Right"
    return "Unknown"


def doi_trang_thai_thanh_chuoi(trang_thai):
    a = doi_list(trang_thai)
    chuoi = ""
    for i in range(3):
        for j in range(3):
            if (a[i][j] == 0):
                chuoi = chuoi + "_ "
            else:
                chuoi = chuoi + str(a[i][j]) + " "
        chuoi = chuoi + "\n"
    return chuoi

def bfs_phien_ban_1(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich = doi_tuple(dich)

    if (node == dich): return [node], 1, "Tìm thấy"

    frontier = Queue()
    frontier.put((node, [node]))
    reached = set()
    reached.add(node)

    so_node = 0

    while (frontier.empty() == False):
        node, duong = frontier.get()
        so_node = so_node + 1
        if (node == dich): return duong, so_node, "Tìm thấy"
        ds_con = tao_con(node)

        for child in ds_con:
            if (child not in reached):
                reached.add(child)
                frontier.put((child, duong + [child]))
    return None, so_node, "Không tìm thấy"

def bfs_phien_ban_2(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich = doi_tuple(dich)
    if (node == dich):
        return [node], 1, "Tìm thấy"
    frontier = Queue()
    frontier.put((node, [node]))

    frontier_set = set()
    frontier_set.add(node)

    explored = set()
    so_node = 0

    while (frontier.empty() == False):
        node, duong = frontier.get()
        frontier_set.remove(node)

        so_node = so_node + 1
        explored.add(node)

        ds_con = tao_con(node)

        for child in ds_con:
            if (child not in explored and child not in frontier_set):
                if (child == dich):
                    return duong + [child], so_node, "Tìm thấy"
                frontier.put((child, duong + [child]))
                frontier_set.add(child)
    return None, so_node, "Không tìm thấy"

def dfs(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich = doi_tuple(dich)
    if (node == dich): return [node], 1, "Tìm thấy"

    frontier = []
    frontier.append((node, [node]))

    reached = set()
    reached.add(node)

    so_node = 0

    while (len(frontier) > 0):
        node, duong = frontier.pop()
        so_node = so_node + 1
        ds_con = tao_con(node)
        for child in ds_con:
            if (child == dich):
                return duong + [child], so_node, "Tìm thấy"
            if (child not in reached):
                reached.add(child)
                frontier.append((child, duong + [child]))
    return None, so_node, "Không tìm thấy"

def depth_limited_search(bat_dau, dich, gioi_han):
    node = doi_tuple(bat_dau)
    dich = doi_tuple(dich)

    frontier = []
    frontier.append((node, [node], 0))
    so_node = 0
    bi_cat = False

    while (len(frontier) > 0):
        node, duong, do_sau = frontier.pop()
        so_node = so_node + 1
        if (node == dich): return duong, so_node, "found"
        if (do_sau >= gioi_han): bi_cat = True
        else:
            ds_con = tao_con(node)
            for child in ds_con:
                if (child not in duong):
                    frontier.append((child, duong + [child], do_sau + 1))
    if (bi_cat == True): return None, so_node, "cutoff"
    return None, so_node, "failure"


def ids(bat_dau, dich):
    tong_node = 0
    max_depth = 40

    for depth in range(max_depth + 1):
        duong, so_node, trang_thai = depth_limited_search(bat_dau, dich, depth)
        tong_node = tong_node + so_node

        if (trang_thai == "found"):
            return duong, tong_node, "Tìm thấy ở depth = " + str(depth)
        if (trang_thai == "failure"):
            return None, tong_node, "Không tìm thấy"
    return None, tong_node, "Không tìm thấy trong max depth = " + str(max_depth)

ds_thuat_toan = [
    ("BFS1", bfs_phien_ban_1),
    ("BFS2", bfs_phien_ban_2),
    ("DFS", dfs),
    ("IDS", ids)
]

def hien_bang(a):
    for i in range(3):
        for j in range(3):
            if (a[i][j] == 0):
                o[i][j].config(text="", bg="#dddddd")
            else:
                o[i][j].config(text=str(a[i][j]), bg="#f7f7f7")

def xoa_log():
    global ds_nuoc_di

    ds_nuoc_di = []

    hop_log.config(state="normal")
    hop_log.delete("1.0", tk.END)

    hop_log.insert(tk.END, "LOG TRẠNG THÁI DI CHUYỂN\n")
    hop_log.insert(tk.END, "Quy ước: L = Left | R = Right | U = Up | D = Down\n")
    hop_log.insert(tk.END, "------------------------------------------------------------\n")

    hop_log.config(state="disabled")


def them_log_bat_dau():
    hop_log.config(state="normal")

    hop_log.insert(tk.END, "Bước 0 | START\n")
    hop_log.insert(tk.END, doi_trang_thai_thanh_chuoi(ket_qua[0]))
    hop_log.insert(tk.END, "------------------------------------------------------------\n")

    hop_log.see(tk.END)
    hop_log.config(state="disabled")


def ghi_lai_chuoi_nuoc_di():
    hop_log.insert(tk.END, "\nChuỗi nước đi:\n")

    if (len(ds_nuoc_di) == 0):
        hop_log.insert(tk.END, "Chưa có nước đi\n")
    else:
        hop_log.insert(tk.END, " -> ".join(ds_nuoc_di) + "\n")


def them_log_buoc_di():
    global ds_nuoc_di

    if (len(ket_qua) == 0): return
    if (buoc <= 0): return

    huong = huong_di_chuyen(ket_qua[buoc - 1], ket_qua[buoc])
    ds_nuoc_di.append(huong)
    hop_log.config(state="normal")

    hop_log.insert(
        tk.END,
        "Bước " + str(buoc)
        + " | Hướng: " + huong
        + " (" + giai_thich_huong(huong) + ")\n"
    )

    hop_log.insert(tk.END, doi_trang_thai_thanh_chuoi(ket_qua[buoc]))
    hop_log.insert(tk.END, "------------------------------------------------------------\n")

    if (buoc == len(ket_qua) - 1):
        ghi_lai_chuoi_nuoc_di()

    hop_log.see(tk.END)
    hop_log.config(state="disabled")

def hien_buoc():
    if (len(ket_qua) == 0):
        thong_bao.config(text="Chưa chạy thuật toán")
        return

    hien_bang(doi_list(ket_qua[buoc]))
    thong_bao.config(
        text=ten_thuat_toan
        + " | Bước "
        + str(buoc)
        + "/"
        + str(len(ket_qua) - 1)
    )

def bam_sinh():
    global bang, ket_qua, buoc, dang_chay, ten_thuat_toan, ds_nuoc_di

    dang_chay = False
    bang = sinh_ma_tran()
    ket_qua = []
    buoc = 0
    ten_thuat_toan = ""
    ds_nuoc_di = []

    hien_bang(bang)
    xoa_log()

    thong_bao.config(text="Đã sinh ma trận mới")


def chay_thuat_toan(ten, ham):
    global ket_qua, buoc, dang_chay, ten_thuat_toan, ds_nuoc_di

    dang_chay = False
    buoc = 0
    ten_thuat_toan = ten
    ds_nuoc_di = []

    thong_bao.config(text="Đang chạy " + ten + "...")
    man_hinh.update()

    ket_qua, so_node, trang_thai = ham(bang, dich)

    xoa_log()

    if (ket_qua == None):
        ket_qua = []

        thong_bao.config(
            text=ten
            + " | "
            + trang_thai
            + " | Node duyệt = "
            + str(so_node)
        )
    else:
        hien_bang(doi_list(ket_qua[0]))

        thong_bao.config(
            text=ten
            + " | Số bước = "
            + str(len(ket_qua) - 1)
            + " | Node duyệt = "
            + str(so_node)
            + " | "
            + trang_thai
        )

        them_log_bat_dau()


def tao_lenh_chay(ten, ham):
    def lenh():
        chay_thuat_toan(ten, ham)

    return lenh


def bam_truoc():
    global buoc

    if (len(ket_qua) == 0):
        thong_bao.config(text="Chưa chạy thuật toán")
        return

    if (buoc > 0):
        buoc = buoc - 1
        hien_buoc()
        thong_bao.config(text="Quay lại bước " + str(buoc) + " | Log không bị xóa")
    else:
        hien_buoc()
        thong_bao.config(text="Đang ở trạng thái bắt đầu")


def bam_tiep():
    global buoc

    if (len(ket_qua) == 0):
        thong_bao.config(text="Chưa chạy thuật toán")
        return

    if (buoc < len(ket_qua) - 1):
        buoc = buoc + 1
        hien_buoc()
        them_log_buoc_di()
    else:
        hien_buoc()
        thong_bao.config(text="Đã tới trạng thái đích")


def doi_toc_do(value):
    global toc_do

    toc_do = int(value)
    thong_bao.config(text="Tốc độ tự động: " + str(toc_do) + " ms")


def tu_dong_chay():
    global buoc, dang_chay

    if (dang_chay == False):
        return

    if (len(ket_qua) == 0):
        thong_bao.config(text="Chưa chạy thuật toán")
        dang_chay = False
        return

    if (buoc < len(ket_qua) - 1):
        buoc = buoc + 1
        hien_buoc()
        them_log_buoc_di()
        man_hinh.after(toc_do, tu_dong_chay)
    else:
        hien_buoc()
        thong_bao.config(text="Đã chạy xong")
        dang_chay = False


def bam_tu_dong():
    global dang_chay

    if (len(ket_qua) == 0):
        thong_bao.config(text="Chưa chạy thuật toán")
        return

    dang_chay = True
    tu_dong_chay()


def bam_dung():
    global dang_chay

    dang_chay = False
    thong_bao.config(text="Đã dừng tự động")


def bam_xoa_log():
    xoa_log()
    thong_bao.config(text="Đã xóa log")

dich = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

bang = [
    [1, 3, 6],
    [8, 0, 7],
    [2, 5, 4]
]

ket_qua = []
buoc = 0
dang_chay = False
toc_do = 700
ten_thuat_toan = ""
ds_nuoc_di = []

man_hinh = tk.Tk()
man_hinh.title("Mô phỏng thuật toán tìm kiếm 8 Puzzle")
man_hinh.geometry("1120x820")
man_hinh.resizable(False, False)

tieu_de = tk.Label(
    man_hinh,
    text="Mô phỏng thuật toán tìm kiếm 8 Puzzle",
    font=("Arial", 18, "bold"),
    fg="#222222"
)
tieu_de.pack(pady=8)

khung_chinh = tk.Frame(man_hinh)
khung_chinh.pack(pady=5)

khung_trai = tk.Frame(
    khung_chinh,
    bd=2,
    relief="groove",
    padx=12,
    pady=10,
    width=720,
    height=720
)
khung_trai.grid(row=0, column=0, padx=10, pady=5, sticky="n")
khung_trai.grid_propagate(False)

nhan_visual = tk.Label(
    khung_trai,
    text="VISUALIZE",
    font=("Arial", 13, "bold"),
    fg="#222222"
)
nhan_visual.pack(pady=3)

khung_bang = tk.Frame(khung_trai, bg="#999999")
khung_bang.pack(pady=8)

o = []

for i in range(3):
    hang = []

    for j in range(3):
        lb = tk.Label(
            khung_bang,
            text="",
            width=4,
            height=2,
            font=("Arial", 24, "bold"),
            relief="ridge",
            bd=2,
            bg="#f7f7f7"
        )

        lb.grid(row=i, column=j, padx=4, pady=4)

        hang.append(lb)

    o.append(hang)

thong_bao = tk.Label(
    khung_trai,
    text="Bấm nút để chạy thuật toán",
    font=("Arial", 11),
    fg="#333333",
    wraplength=650,
    justify="center"
)
thong_bao.pack(pady=5)

nhan_log = tk.Label(
    khung_trai,
    text="Log trạng thái nước đi",
    font=("Arial", 12, "bold"),
    fg="#222222"
)
nhan_log.pack(pady=3)

khung_log = tk.Frame(khung_trai)
khung_log.pack(pady=5)

thanh_cuon_doc = tk.Scrollbar(khung_log, orient="vertical")
thanh_cuon_doc.grid(row=0, column=1, sticky="ns")

thanh_cuon_ngang = tk.Scrollbar(khung_log, orient="horizontal")
thanh_cuon_ngang.grid(row=1, column=0, sticky="ew")

hop_log = tk.Text(
    khung_log,
    width=82,
    height=15,
    font=("Consolas", 10),
    bg="#f5f5f5",
    fg="#222222",
    relief="ridge",
    bd=2,
    wrap="none",
    yscrollcommand=thanh_cuon_doc.set,
    xscrollcommand=thanh_cuon_ngang.set
)
hop_log.grid(row=0, column=0)

thanh_cuon_doc.config(command=hop_log.yview)
thanh_cuon_ngang.config(command=hop_log.xview)

hop_log.config(state="disabled")

khung_phai = tk.Frame(
    khung_chinh,
    bd=2,
    relief="groove",
    padx=10,
    pady=10,
    width=250,
    height=720
)
khung_phai.grid(row=0, column=1, padx=10, pady=5, sticky="n")
khung_phai.grid_propagate(False)

nhan_dieu_khien = tk.Label(
    khung_phai,
    text="ĐIỀU KHIỂN",
    font=("Arial", 13, "bold"),
    fg="#222222"
)
nhan_dieu_khien.pack(pady=3)

nut_sinh = tk.Button(
    khung_phai,
    text="Sinh ma trận",
    font=("Arial", 10),
    width=18,
    command=bam_sinh
)
nut_sinh.pack(pady=4)

nhan_thuat_toan = tk.Label(
    khung_phai,
    text="Thuật toán",
    font=("Arial", 11, "bold"),
    fg="#333333"
)
nhan_thuat_toan.pack(pady=6)

for ten, ham in ds_thuat_toan:
    nut = tk.Button(
        khung_phai,
        text=ten,
        font=("Arial", 10),
        width=18,
        command=tao_lenh_chay(ten, ham)
    )

    nut.pack(pady=3)

nhan_buoc = tk.Label(
    khung_phai,
    text="Chạy từng bước",
    font=("Arial", 11, "bold"),
    fg="#333333"
)
nhan_buoc.pack(pady=6)

nut_truoc = tk.Button(
    khung_phai,
    text="Bước trước",
    font=("Arial", 10),
    width=18,
    command=bam_truoc
)
nut_truoc.pack(pady=3)

nut_tiep = tk.Button(
    khung_phai,
    text="Bước sau",
    font=("Arial", 10),
    width=18,
    command=bam_tiep
)
nut_tiep.pack(pady=3)

nut_auto = tk.Button(
    khung_phai,
    text="Tự động chạy",
    font=("Arial", 10),
    width=18,
    command=bam_tu_dong
)
nut_auto.pack(pady=3)

nut_dung = tk.Button(
    khung_phai,
    text="Dừng",
    font=("Arial", 10),
    width=18,
    command=bam_dung
)
nut_dung.pack(pady=3)

nut_xoa_log = tk.Button(
    khung_phai,
    text="Xóa log",
    font=("Arial", 10),
    width=18,
    command=bam_xoa_log
)
nut_xoa_log.pack(pady=3)

toc_do_chay = tk.Scale(
    khung_phai,
    from_=100,
    to=2000,
    orient="horizontal",
    label="Tốc độ tự động chạy (ms)",
    command=doi_toc_do,
    length=180
)
toc_do_chay.set(700)
toc_do_chay.pack(pady=5)

hien_bang(bang)
xoa_log()

man_hinh.mainloop()