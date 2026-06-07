# 8-Puzzle Search Algorithm Visualizer (BTVN 11)

Phần mềm trực quan hóa các thuật toán tìm kiếm giải bài toán 8-Puzzle, được cập nhật thêm **Thuật toán Luyện thép (Simulated Annealing)** và hỗ trợ **Tìm kiếm trong môi trường không nhìn thấy (Belief State / Sensorless Search)**.

---

## Cấu trúc Mã nguồn Mới
Để dễ quản lý và chỉnh sửa, các thuật toán đã được viết riêng ra từng file trong thư mục `algorithms/`:
- `algorithms/common.py`: Các hàm tiện ích dùng chung (di chuyển, sinh ma trận, khoảng cách Manhattan, số ô sai...).
- `algorithms/bfs.py`: Thuật toán BFS (Version 1 & 2).
- `algorithms/dfs.py`: Thuật toán DFS.
- `algorithms/ids.py`: Thuật toán IDS (Iterative Deepening Search).
- `algorithms/ucs.py`: Thuật toán UCS (Uniform Cost Search).
- `algorithms/greedy.py`: Thuật toán Greedy Best-First Search.
- `algorithms/astar.py`: Thuật toán A*.
- `algorithms/idastar.py`: Thuật toán IDA*.
- `algorithms/hill_climbing.py`: Các biến thể Hill Climbing (Leo đồi dốc nhất, Leo đồi ngẫu nhiên, Lặp lại ngẫu nhiên...).
- `algorithms/beam_search.py`: Thuật toán Local Beam Search.
- `algorithms/simulated_annealing.py`: Thuật toán Luyện thép thường và Luyện thép cho Trạng thái Belief.

---

## Các Thuật toán Mới & Tính năng Nâng cao

### 1. Thuật toán Luyện thép (Simulated Annealing)
- Mô phỏng quá trình luyện thép vật lý. Tại mỗi bước, chọn ngẫu nhiên một trạng thái lân cận.
- Nếu lân cận tốt hơn (giảm Heuristic), chấp nhận di chuyển.
- Nếu tệ hơn, chấp nhận di chuyển với xác suất $p = \exp(-\Delta / T)$ để thoát khỏi cực trị cục bộ.
- Nhiệt độ giảm dần sau mỗi bước theo hệ số làm nguội $\alpha$ ($T = \alpha \times T$).

### 2. Tìm kiếm trong Môi trường không nhìn thấy (Belief State Search)
Hỗ trợ giải bài toán 8-Puzzle khi một phần hoặc toàn bộ thông tin của Start hoặc Goal bị khuyết (ẩn):
- **Khuyết hoàn toàn Start**: Vị trí các ô số ở trạng thái bắt đầu hoàn toàn ẩn (`?`). Chương trình sinh ra $k$ trạng thái belief ngẫu nhiên giải được. Chuỗi hành động tìm được phải đưa tất cả $k$ trạng thái này hội tụ về cùng một trạng thái đích duy nhất.
- **Khuyết hoàn toàn Goal**: Trạng thái đích hoàn toàn ẩn. Chương trình sinh ra $k$ trạng thái đích ngẫu nhiên. Tất cả $k$ trạng thái bắt đầu phải hội tụ về cùng một trạng thái đích trong số đó.
- **Khuyết một phần (Start & Goal)**: Người dùng có thể thiết lập số lượng ô ẩn ngẫu nhiên (hiển thị dạng `?`). Chương trình sinh ra $k$ trạng thái bắt đầu và $k$ trạng thái đích tương thích để tìm kiếm đường đi hội tụ.

Heuristic sử dụng cho belief state $B$ và tập đích $G$:
$$h(B) = \min_{g \in G} \sum_{s \in B} \text{ManhattanDistance}(s, g)$$

---

## Giao diện Trực quan hóa Mới (Simulation Window)
Khi chọn thuật toán, chương trình sẽ mở ra một **Cửa sổ Mô phỏng Mới (Toplevel Window)** để dễ dàng quan sát:
1. **Trực quan hóa Song song**: Hiển thị đồng thời cả $k$ bàn cờ 8-puzzle để người dùng theo dõi cách các trạng thái di chuyển đồng bộ và hội tụ về đích.
2. **Biểu đồ Động (Live Chart)**: Canvas tự vẽ thể hiện đường biểu diễn Heuristic giảm dần và Nhiệt độ $T$ hạ dần theo thời gian thực.
3. **Bộ điều khiển**: Tự động chạy (Auto-run), Tạm dừng (Pause), Tiến/Lùi từng bước (Step forward/backward) và thanh trượt tốc độ.
4. **Log chi tiết**: Ghi nhận chi tiết từng bước di chuyển, hành động (U, D, L, R) áp dụng lên belief state, và in chuỗi nước đi hoàn chỉnh khi kết thúc.

---

## Hướng dẫn sử dụng
1. Mở terminal tại thư mục chứa file mã nguồn.
2. Chạy lệnh sau để khởi động ứng dụng:
   ```bash
   python 24162039_NguyenDucHoc_8puzzle_Visualize.py
   ```
3. Thiết lập chế độ môi trường (Quan sát đầy đủ / Khuyết Start / Khuyết Goal / Khuyết 1 phần).
4. Thiết lập số lượng $k$ (belief state size) và các tham số Luyện thép ($T_0, T_{min}, \alpha$).
5. Bấm vào bất kỳ thuật toán nào để mở cửa sổ mô phỏng và bắt đầu chạy!