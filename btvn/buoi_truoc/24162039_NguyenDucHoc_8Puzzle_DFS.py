import random
import tkinter as tk
from queue import Queue

def rule(x,y):
    moves = []
    if (x==0 and y==0):
        moves = [(0,1), (1,0)]
    elif (x==0 and y==1):
        moves = [(0,0), (0,2), (1,1)]
    elif (x==0 and y==2):
        moves = [(0,1), (1,2)]
    elif (x==1 and y==0):
        moves = [(0,0), (1,1), (2,0)]
    elif (x==1 and y==1):
        moves = [(0,1), (1,0), (1,2), (2,1)]
    elif (x==1 and y==2):
        moves = [(0,2), (1,1), (2,2)]
    elif (x==2 and y==0):
        moves = [(1,0), (2,1)]
    elif (x==2 and y==1):
        moves = [(1,1), (2,0), (2,2)]
    else:
        moves = [(2,1), (1,2)]
    return moves

def tim_so_0(a):
    for i in range(3):
        for j in range(3):
            if(a[i][j]==0):
                return i,j

def doi_tuple(a):
    b=[]
    for i in range(3):
        hang=[]
        for j in range(3):
            hang.append(a[i][j])
        b.append(tuple(hang))
    return tuple(b)

def doi_list(a):
    b=[]
    for i in range(3):
        hang=[]
        for j in range(3):
            hang.append(a[i][j])
        b.append(hang)
    return b

def dem_nghich_the(a):
    b=[]
    for i in range(3):
        for j in range(3):
            if(a[i][j]!=0):
                b.append(a[i][j])

    dem=0
    for i in range(len(b)):
        for j in range(i+1,len(b)):
            if(b[i]>b[j]):
                dem=dem+1
    return dem

def co_giai_duoc(a):
    if(dem_nghich_the(a)%2==0):
        return True
    return False

def sinh_ma_tran():
    so=[0,1,2,3,4,5,6,7,8]
    while(True):
        random.shuffle(so)
        a=[];k=0
        for i in range(3):
            hang=[]
            for j in range(3):
                hang.append(so[k])
                k=k+1
            a.append(hang)
        if(co_giai_duoc(a)==True):
            return a

def tao_con(trang_thai):
    a=doi_list(trang_thai)
    x,y=tim_so_0(a)
    ds_con=[]

    for dx,dy in rule(x,y):
        b=doi_list(trang_thai)
        b[x][y],b[dx][dy]=b[dx][dy],b[x][y]
        ds_con.append(doi_tuple(b))
    return ds_con

def dfs(bat_dau, dich):
    node = doi_tuple(bat_dau)
    dich = doi_tuple(dich)

    if node == dich:
        return [node], 1

    frontier = []
    frontier.append((node, [node]))
    reached = set()
    reached.add(node)
    so_node = 0
    while len(frontier) > 0:
        node, duong = frontier.pop()
        so_node += 1
        ds_con = tao_con(node)

        for child in ds_con:
            if child == dich:
                return duong + [child], so_node

            if child not in reached:
                reached.add(child)
                frontier.append((child, duong + [child]))
    return None, so_node

def hien_bang(a):
    for i in range(3):
        for j in range(3):
            if(a[i][j]==0):
                o[i][j].config(text="",bg="#dddddd")
            else:
                o[i][j].config(text=str(a[i][j]),bg="#f7f7f7")

def bam_sinh():
    global bang,ket_qua,buoc,dang_chay

    dang_chay=False
    bang=sinh_ma_tran()
    ket_qua=[]
    buoc=0

    hien_bang(bang)
    thong_bao.config(text="Đã sinh ma trận mới")

def bam_dfs():
    global ket_qua,buoc,dang_chay

    dang_chay=False
    thong_bao.config(text="Đang chạy DFS...")
    man_hinh.update()

    ket_qua,so_node=dfs(bang,dich)
    buoc=0

    if(ket_qua==None):
        thong_bao.config(text="DFS không tìm thấy")
    else:
        thong_bao.config(text="DFS: số bước = "+str(len(ket_qua)-1)+" | node duyệt = "+str(so_node))
        hien_bang(doi_list(ket_qua[0]))

def hien_buoc():
    if(len(ket_qua)==0):
        thong_bao.config(text="Chưa chạy DFS")
        return

    hien_bang(doi_list(ket_qua[buoc]))
    thong_bao.config(text="Đang ở bước "+str(buoc)+"/"+str(len(ket_qua)-1))

def bam_tiep():
    global buoc

    if(len(ket_qua)==0):
        thong_bao.config(text="Chưa chạy DFS")
        return

    if(buoc<len(ket_qua)-1):
        buoc=buoc+1
        hien_buoc()
    else:
        hien_buoc()
        thong_bao.config(text="Đã tới trạng thái đích")

def bam_truoc():
    global buoc

    if(len(ket_qua)==0):
        thong_bao.config(text="Chưa chạy DFS")
        return

    if(buoc>0):
        buoc=buoc-1
        hien_buoc()
    else:
        hien_buoc()
        thong_bao.config(text="Đang ở trạng thái bắt đầu")

def doi_toc_do(value):
    global toc_do
    toc_do=int(value)
    thong_bao.config(text="Tốc độ tự động: "+str(toc_do)+" ms")

def tu_dong_chay():
    global buoc,dang_chay

    if(dang_chay==False):
        return

    if(len(ket_qua)==0):
        thong_bao.config(text="Chưa chạy DFS")
        dang_chay=False
        return

    if(buoc<len(ket_qua)-1):
        buoc=buoc+1
        hien_buoc()
        man_hinh.after(toc_do,tu_dong_chay)
    else:
        hien_buoc()
        thong_bao.config(text="Đã chạy xong")
        dang_chay=False

def bam_tu_dong():
    global dang_chay

    if(len(ket_qua)==0):
        thong_bao.config(text="Chưa chạy DFS")
        return

    dang_chay=True
    tu_dong_chay()

def bam_dung():
    global dang_chay

    dang_chay=False
    thong_bao.config(text="Đã dừng tự động")

dich=[
    [1,2,3],
    [4,5,6],
    [7,8,0]
]

bang=[
    [1,2,3],
    [4,0,6],
    [7,5,8]
]

ket_qua=[]; buoc=0; dang_chay=False; toc_do=700

man_hinh=tk.Tk()
man_hinh.title("Mô phỏng DFS 8 Puzzle")
man_hinh.geometry("480x560")

tieu_de=tk.Label(man_hinh,text="8 Puzzle - DFS",font=("Arial",18,"bold"),fg="#222222")
tieu_de.pack(pady=6)

khung=tk.Frame(man_hinh,bg="#999999")
khung.pack(pady=6)

o=[]

for i in range(3):
    hang=[]
    for j in range(3):
        lb=tk.Label(
            khung,
            text="",
            width=3,
            height=1,
            font=("Arial",24,"bold"),
            relief="ridge",
            bd=2,
            bg="#f7f7f7"
        )
        lb.grid(row=i,column=j,padx=3,pady=3)
        hang.append(lb)
    o.append(hang)

thong_bao=tk.Label(man_hinh,text="Bấm nút để chạy",font=("Arial",11),fg="#333333")
thong_bao.pack(pady=5)

khung_nut=tk.Frame(man_hinh)
khung_nut.pack(pady=5)

nut_sinh=tk.Button(khung_nut,text="Sinh ma trận",font=("Arial",10),width=13,command=bam_sinh)
nut_sinh.grid(row=0,column=0,padx=3,pady=3)

# nut_bfs1=tk.Button(khung_nut,text="BFS 1",font=("Arial",10),width=13,command=bam_bfs1)
# nut_bfs1.grid(row=0,column=1,padx=3,pady=3)

nut_bfs2=tk.Button(khung_nut,text="DFS",font=("Arial",10),width=13,command=bam_dfs)
nut_bfs2.grid(row=0,column=2,padx=3,pady=3)

nut_truoc=tk.Button(khung_nut,text="Bước trước",font=("Arial",10),width=13,command=bam_truoc)
nut_truoc.grid(row=1,column=0,padx=3,pady=3)

nut_tiep=tk.Button(khung_nut,text="Bước sau",font=("Arial",10),width=13,command=bam_tiep)
nut_tiep.grid(row=1,column=1,padx=3,pady=3)

nut_auto=tk.Button(khung_nut,text="Tự động chạy",font=("Arial",10),width=13,command=bam_tu_dong)
nut_auto.grid(row=1,column=2,padx=3,pady=3)

nut_dung=tk.Button(khung_nut,text="Dừng",font=("Arial",10),width=13,command=bam_dung)
nut_dung.grid(row=2,column=1,padx=3,pady=3)

toc_do_chay=tk.Scale(
    man_hinh,
    from_=100,
    to=2000,
    orient="horizontal",
    label="Tốc độ tự động chạy (ms)",
    command=doi_toc_do,
    length=250
)
toc_do_chay.set(700)
toc_do_chay.pack(pady=3)

# ghi_chu=tk.Label(
#     man_hinh,
#     text="BFS 1: gặp goal đưa vào queue, khi lấy ra được mới dừng\nBFS 2: sinh child gặp goal thì dừng luôn",
#     font=("Arial",9),
#     fg="#555555"
# )
# ghi_chu.pack(pady=5)

hien_bang(bang)
man_hinh.mainloop()