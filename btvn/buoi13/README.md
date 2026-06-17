# 8-Puzzle Search Algorithm Visualizer (BTVN 13)

Phần mềm trực quan hóa các thuật toán tìm kiếm giải bài toán 8-Puzzle, được cập nhật thêm **AC-3**, **Min-Conflicts** và hỗ trợ **Tìm kiếm trong môi trường không nhìn thấy (Belief State / Sensorless Search)**.

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
- `algorithms/and_or_search.py`: Thuật toán AND-OR Graph Search.
- `algorithms/backtracking_search.py`: Thuật toán Backtracking Search (CSP).
- `algorithms/forward_checking.py`: Thuật toán Forward Checking (CSP).
- `algorithms/ac3.py`: Thuật toán AC-3 (Arc Consistency 3).
- `algorithms/min_conflicts.py`: Thuật toán Min-Conflicts.

---

## Các Thuật toán Mới & Tính năng Nâng cao

### 1. Thuật toán Luyện thép (Simulated Annealing)
- Mô phỏng quá trình luyện thép vật lý. Tại mỗi bước, chọn ngẫu nhiên một trạng thái lân cận.
- Nếu lân cận tốt hơn (giảm Heuristic), chấp nhận di chuyển.
- Nếu tệ hơn, chấp nhận di chuyển với xác suất $p = \exp(-\Delta / T)$ để thoát khỏi cực trị cục bộ.
- Nhiệt độ giảm dần sau mỗi bước theo hệ số làm nguội $\alpha$ ($T = \alpha \times T$).

### 2. Thuật toán AND-OR Graph Search
- Thực hiện tìm kiếm trên đồ thị AND-OR trong môi trường 8-Puzzle (và môi trường Belief State). Kế hoạch tìm kiếm được phân rã thành các nhánh điều kiện hành động và trạng thái tương ứng.

### 3. Các Thuật toán CSP (Constraint Satisfaction Problem)
- **Backtracking CSP**: Thuật toán thử gán tuần tự các giá trị cho các ô trống và quay lui nếu phát hiện vi phạm.
- **Forward Checking**: Kết hợp lan truyền ràng buộc (Constraint Propagation) thu hẹp miền giá trị của các ô chưa gán ngay sau mỗi bước gán, giúp cắt tỉa sớm các nhánh tìm kiếm vô ích.
- **AC-3 (Arc Consistency 3)**: Xây dựng tập hợp các cung (arcs) giữa các biến và loại bỏ các giá trị không hợp lệ trong Domain nhằm giảm thiểu kích thước không gian trạng thái từ sớm. 
- **Min-Conflicts**: Thuật toán tìm kiếm cục bộ cho CSP. Khởi tạo bằng một bảng phân bổ ngẫu nhiên (cho phép vi phạm luật). Hệ thống lần lượt chọn các ô xung đột và đổi sang giá trị ít gây xung đột nhất cho đến khi tìm ra cấu hình đích.

### 4. Tìm kiếm trong Môi trường không nhìn thấy (Belief State Search)
Hỗ trợ giải bài toán 8-Puzzle khi một phần hoặc toàn bộ thông tin của Start hoặc Goal bị khuyết (ẩn):
- **Khuyết hoàn toàn Start**: Vị trí các ô số ở trạng thái bắt đầu hoàn toàn ẩn (`?`). Chương trình sinh ra $k$ trạng thái belief ngẫu nhiên giải được. Chuỗi hành động tìm được phải đưa tất cả $k$ trạng thái này hội tụ về cùng một trạng thái đích duy nhất.
- **Khuyết hoàn toàn Goal**: Trạng thái đích hoàn toàn ẩn. Chương trình sinh ra $k$ trạng thái đích ngẫu nhiên. Tất cả $k$ trạng thái bắt đầu phải hội tụ về cùng một trạng thái đích trong số đó.
- **Khuyết một phần (Start & Goal)**: Người dùng có thể thiết lập số lượng ô ẩn ngẫu nhiên (hiển thị dạng `?`). Chương trình sinh ra $k$ trạng thái bắt đầu và $k$ trạng thái đích tương thích để tìm kiếm đường đi hội tụ.

Heuristic sử dụng cho belief state $B$ và tập đích $G$:
$$h(B) = \min_{g \in G} \sum_{s \in B} \text{ManhattanDistance}(s, g)$$

### 5. Nhập Ma trận Thủ công
- Cung cấp giao diện Popup cho phép người dùng tự nhập trực tiếp 9 số (0-8) vào lưới 3x3 để tạo trạng thái xuất phát theo ý muốn.
- Tự động kiểm tra tính hợp lệ của giá trị (đủ 9 số, không trùng lặp, nằm trong khoảng 0-8).

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
3. Sử dụng nút **Sinh ma trận ngẫu nhiên** hoặc **Nhập ma trận** để thiết lập bảng.
4. Thiết lập chế độ môi trường (Quan sát đầy đủ / Khuyết Start / Khuyết Goal / Khuyết 1 phần).
5. Thiết lập số lượng $k$ (belief state size) và các tham số Luyện thép ($T_0, T_{min}, \alpha$).
6. Cột công cụ bên phải đã được trang bị **Thanh cuộn dọc** để hiển thị tất cả các thuật toán. Bấm vào bất kỳ thuật toán nào để mở cửa sổ mô phỏng và bắt đầu chạy!