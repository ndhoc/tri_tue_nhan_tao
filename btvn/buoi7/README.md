# Bài tập buổi 7 - Mô phỏng 8-Puzzle nâng cao

Phiên bản nâng cấp của ứng dụng mô phỏng 8-Puzzle, bổ sung thêm các thuật toán tìm kiếm có trọng số và heuristic.

## File code
- `24162039_NguyenDucHoc_Visualize_8Puzzle_2BFS_DFS_IDS_UCS_GS.py`: Mã nguồn Python (Tkinter + Multi-threading).

## Thuật toán tích hợp
1. **BFS Version 1 & 2** (Breadth-First Search)
2. **DFS** (Depth-First Search)
3. **IDS** (Iterative Deepening Search)
4. **UCS** (Uniform Cost Search)
5. **Greedy Search** (Tìm kiếm tham lam với heuristic Manhattan Distance)

## Cải tiến
- Giao diện đẹp hơn với `tkinter.ttk`.
- Chạy thuật toán ở một Thread riêng biệt (`threading`) tránh đơ giao diện khi duyệt quá nhiều node.
- Hiển thị chi tiết Cost, Max Depth và giá trị Heuristic h(n) trong log.
