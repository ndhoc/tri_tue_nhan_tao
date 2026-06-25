# Mô phỏng trò chơi 8 Puzzle BFS

Chương trình mô phỏng bài toán 8-Puzzle bằng thuật toán BFS, sử dụng GUI bằng Python Tkinter.

## Chức năng

- Hiển thị bàn cờ 8-Puzzle dạng ma trận 3x3.

- Sinh ma trận ngẫu nhiên có thể giải được.

- Mô phỏng 2 phiên bản BFS:

  - BFS 1: kiểm tra trạng thái mục tiêu khi lấy node ra khỏi hàng đợi.

  - BFS 2: kiểm tra trạng thái mục tiêu ngay khi sinh node con.

- Hiển thị số bước đi và số node đã duyệt.

- Có nút xem từng bước di chuyển từ trạng thái ban đầu đến trạng thái đích, nút xem trạng thái trước đó, nút tự động chạy kèm với thanh tốc độ chạy.

## Trạng thái đích

```python
[
    [1,2,3],
    [4,5,6],
    [7,8,0]
]
```

## Chạy chương trình

```bash
python main.py
```

## Nguồn tham khảo

[GeeksforGeeks - Python Tkinter Tutorial](https://www.geeksforgeeks.org/python/python-tkinter-tutorial/)