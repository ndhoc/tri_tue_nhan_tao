# 📚 Báo Cáo Bài Tập Về Nhà - Môn Trí Tuệ Nhân Tạo

**Repository này chứa toàn bộ quá trình thực hiện bài tập về nhà (BTVN) môn Trí Tuệ Nhân Tạo, từ những mô phỏng cơ bản đầu tiên đến việc xây dựng một hệ thống trực quan hóa (Visualizer) hoàn chỉnh cho bài toán 8-Puzzle với đa dạng các thuật toán tìm kiếm AI.**

---

## 👨‍🎓 Thông Tin Sinh Viên

- **Họ và Tên:** Nguyễn Đức Học
- **Mã số sinh viên:** 24162039
- **Môn học:** Trí Tuệ Nhân Tạo

---

## 📂 Tổng Quan Cấu Trúc Thư Mục (`btvn`)

Phần bài tập được tổ chức theo từng buổi học (từ Buổi 3 đến Buổi 13), thể hiện sự phát triển và nâng cấp dần của hệ thống qua từng tuần:

- **Buổi 3** ([`btvn/buoi3/`](./btvn/buoi3/)): Mô phỏng Robot hút bụi cơ bản với tác tử phản xạ đơn giản (**Simple Reflex Agent**).
- **Buổi 4** ([`btvn/buoi4/`](./btvn/buoi4/)): Nâng cấp Robot hút bụi với tác tử dựa trên mô hình (**Model-based Agent**).
- **Buổi 5** ([`btvn/buoi5/`](./btvn/buoi5/)): Khởi tạo dự án **8-Puzzle Visualizer**. Cài đặt thuật toán Tìm kiếm theo chiều rộng (**BFS**).
- **Buổi 6** ([`btvn/buoi6/`](./btvn/buoi6/)): Tích hợp thuật toán Tìm kiếm theo chiều sâu (**DFS**) và Tìm kiếm sâu dần (**IDS**).
- **Buổi 7** ([`btvn/buoi7/`](./btvn/buoi7/)): Thêm thuật toán Tìm kiếm chi phí đồng nhất (**UCS**) và Tìm kiếm tham lam (**Greedy Best-First Search**).
- **Buổi 8** ([`btvn/buoi8/`](./btvn/buoi8/)): Hoàn thiện nhóm thuật toán tìm kiếm có thông tin với **A*** và **IDA***.
- **Buổi 9** ([`btvn/buoi9/`](./btvn/buoi9/)): Chuyển sang nhóm thuật toán Tìm kiếm cục bộ (**Local Search**), cài đặt **Hill Climbing** (Leo đồi dốc nhất).
- **Buổi 10** ([`btvn/buoi10/`](./btvn/buoi10/)): Mở rộng Local Search với các biến thể: **Stochastic Hill Climbing**, **Random Restart Hill Climbing** và **Local Beam Search**.
- **Buổi 11** ([`btvn/buoi11/`](./btvn/buoi11/)): Cài đặt thuật toán Luyện thép (**Simulated Annealing**) và bước đầu xử lý môi trường không xác định với **Belief State / Sensorless Search**.
- **Buổi 12** ([`btvn/buoi12/`](./btvn/buoi12/)): Tích hợp thuật toán tìm kiếm trên đồ thị **AND-OR**. Mở rộng sang bài toán thỏa mãn ràng buộc (CSP) với **Backtracking** và **Forward Checking**.
- **Buổi 13** ([`btvn/buoi13/`](./btvn/buoi13/)): Phiên bản Final. Tái cấu trúc mã nguồn theo dạng Module (thư mục `algorithms/`). Thêm thuật toán **AC-3**, **Min-Conflicts** và nâng cấp hệ thống mô phỏng đồ họa.

---

## 🚀 Các Tính Năng Nổi Bật (Phiên Bản Hoàn Thiện - Buổi 13)

Phiên bản cuối cùng tại thư mục `buoi13` là một ứng dụng Desktop hoàn chỉnh với các tính năng:

1. **Hệ sinh thái thuật toán đa dạng (18+ thuật toán):**
   - **Uninformed Search:** BFS, DFS, IDS, UCS.
   - **Informed Search:** Greedy, A*, IDA*.
   - **Local Search:** Hill Climbing (nhiều biến thể), Local Beam Search, Simulated Annealing.
   - **CSP (Constraint Satisfaction Problem):** Backtracking, Forward Checking, AC-3, Min-Conflicts.
   - **Complex Environment:** Partial Observable, No Observable, AND-OR Graph Search.

2. **Tìm kiếm trong Môi trường Phức Tạp (Belief State / Sensorless Search):**
   - Hỗ trợ các kịch bản: Khuyết hoàn toàn trạng thái Bắt đầu (Start), Khuyết Goal, hoặc Khuyết ngẫu nhiên (ẩn dưới dạng `?`).
   - Khả năng xử lý $k$ trạng thái Belief đồng thời và tìm đường đi hội tụ về đích chung.

3. **Giao diện Trực quan hóa Cao cấp (Toplevel Simulation Window):**
   - Mô phỏng trực tiếp quá trình di chuyển của các ô số.
   - Hiển thị song song nhiều bàn cờ (đối với Belief State).
   - **Live Chart**: Đồ thị vẽ theo thời gian thực thể hiện sự giảm dần của giá trị Heuristic và Nhiệt độ $T$ (trong Simulated Annealing).
   - Bộ điều khiển phát/tạm dừng (Auto-run, Pause), tiến/lùi từng bước (Step forward/backward), và điều chỉnh tốc độ mượt mà.
   - Log chi tiết từng bước đi (U, D, L, R) cho mục đích theo dõi và học tập.

4. **Quản lý mã nguồn Module hóa:** Toàn bộ thuật toán được tách riêng vào thư mục `algorithms/`, giúp dễ dàng đọc hiểu, bảo trì và mở rộng code độc lập với UI.

---

## 🛠️ Hướng Dẫn Cài Đặt và Chạy Chương Trình

Để trải nghiệm toàn bộ các tính năng mới nhất, vui lòng chạy phiên bản của **Buổi 13**.

### 1. Yêu cầu môi trường
- Cài đặt [Python 3.x](https://www.python.org/downloads/) trên máy tính.
- Các thư viện tiêu chuẩn của Python (Tkinter tích hợp sẵn). Nếu báo lỗi thiếu thư viện hình ảnh có thể cần cài thêm Pillow (`pip install Pillow`).

### 2. Khởi chạy ứng dụng (Phiên bản đầy đủ nhất)
Mở Terminal/Command Prompt, di chuyển vào thư mục repo này và chạy lệnh sau:

```bash
cd btvn/buoi13
python 24162039_NguyenDucHoc_8puzzle_Visualize.py
```

### 3. Cách sử dụng
- **Thiết lập trạng thái:** Chọn "Sinh ma trận ngẫu nhiên" hoặc tự nhập ma trận 3x3 theo ý muốn.
- **Chọn môi trường:** Có thể chọn chế độ quan sát đầy đủ hoặc các chế độ khuyết (Belief State).
- **Chọn thuật toán:** Cột bên phải hiển thị danh sách tất cả các thuật toán đã học. Bấm vào một thuật toán bất kỳ, cửa sổ Mô phỏng sẽ hiện lên.
- **Điều khiển:** Sử dụng các nút điều khiển bên trong cửa sổ mô phỏng để chạy, tạm dừng hoặc xem chi tiết từng bước.

---

> Em xin gửi lời cảm ơn tới Cô đã tận tình giảng dạy và hướng dẫn trong suốt quá trình học tập. Toàn bộ mã nguồn được em tự xây dựng và tinh chỉnh dần qua từng buổi dựa trên kiến thức đã học, kết hợp với các tài liệu tham khảo để mang lại hệ thống mô phỏng và học tập tốt nhất cho các thuật toán AI.
