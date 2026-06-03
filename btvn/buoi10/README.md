# 8-Puzzle Search Algorithm Visualizer

Phần mềm trực quan hóa các thuật toán tìm kiếm giải bài toán 8-Puzzle.

---

## Các thuật toán được trực quan hóa

Chương trình hỗ trợ mô phỏng **13 thuật toán tìm kiếm** từ mù (Uninformed), có hướng dẫn (Informed/Heuristic) cho đến tìm kiếm cục bộ (Local Search):

1. **BFS Version 1**: Tìm kiếm theo chiều rộng (kiểm tra đích khi lấy nút ra khỏi hàng đợi).
2. **BFS Version 2**: Tìm kiếm theo chiều rộng (kiểm tra đích ngay khi sinh ra trạng thái con).
3. **DFS (Depth-First Search)**: Tìm kiếm theo chiều sâu.
4. **IDS (Iterative Deepening Search)**: Tìm kiếm sâu dần.
5. **UCS (Uniform Cost Search)**: Tìm kiếm với chi phí đồng nhất (Uniform Cost).
6. **Greedy Search (Greedy Best-First Search)**: Tìm kiếm tham lam (sử dụng hàm khoảng cách Manhattan làm Heuristic $h(n)$).
7. **A\***: Tìm kiếm A* tối ưu (kết hợp chi phí thực tế $g(n)$ dựa trên số ô sai và heuristic Manhattan $h(n)$).
8. **IDA\* (Iterative Deepening A\*)**: Tìm kiếm A* sâu dần.
9. **Local Search (First-Choice Hill Climbing)**: Tìm kiếm cục bộ di chuyển nhanh. Duyệt các trạng thái lân cận, chọn ngay trạng thái đầu tiên có chi phí (số ô sai không tính 0) nhỏ hơn trạng thái hiện tại.
10. **Simple Hill Climbing (Steepest Descent)**: Tìm kiếm leo đồi chọn độ dốc nhất. Duyệt tất cả các trạng thái lân cận, chọn trạng thái có chi phí nhỏ nhất và nhỏ hơn trạng thái hiện tại, lặp lại cho đến khi tìm được đích hoặc bị kẹt ở cực trị cục bộ.
11. **Stochastic Hill Climbing**: Leo đồi ngẫu nhiên. Sinh ra các trạng thái lân cận của trạng thái hiện tại, sau đó lọc những trạng thái tốt hơn trạng thái hiện tại (khoảng cách Manhattan nhỏ hơn) vào tập `Better_Neighbors`, rồi chọn ngẫu nhiên một trạng thái trong đó làm trạng thái tiếp theo.
12. **Random Restart Hill Climbing**: Leo đồi lặp lại ngẫu nhiên. Chạy leo đồi ngẫu nhiên (Stochastic Hill Climbing) tối đa `Max Restart` lần. Ở mỗi lượt, bắt đầu lại từ cùng một trạng thái. Nếu tìm thấy đích, trả về kết quả; nếu hết lượt mà không tìm thấy đích, trả về lượt tốt nhất.
13. **Local Beam Search**: Tìm kiếm chùm cục bộ. Bắt đầu với một chùm gồm `k` trạng thái (gồm trạng thái ban đầu và `k-1` trạng thái sinh ngẫu nhiên từ trạng thái ban đầu bằng các bước đi ngẫu nhiên). Ở mỗi bước, sinh ra tất cả các trạng thái lân cận từ các trạng thái trong chùm, sắp xếp chúng theo khoảng cách Manhattan tăng dần, và chọn ra `k` trạng thái tốt nhất làm chùm mới.

---

## Tính năng nổi bật

- **Giao diện hiện đại & Thân thiện**: Tông màu sáng thanh lịch, font chữ Segoe UI sắc nét, bố cục rõ ràng giữa bảng điều khiển, bàn cờ 8-puzzle và khu vực Log hoạt động.
- **Sinh ma trận ngẫu nhiên thông minh**: Đảm bảo ma trận sinh ra **luôn luôn giải được** bằng cách kiểm tra số nghịch thế (Inversion Count).
- **Xử lý đa luồng (Multi-threading)**: Thuật toán tìm kiếm chạy ở luồng nền (background thread), giúp giao diện không bị đơ/treo (freeze) kể cả với các thuật toán tốn thời gian như DFS hay IDS.
- **Điều khiển mô phỏng linh hoạt**:
  - Chạy tự động (**Tự động chạy**) hoặc tạm dừng (**Dừng**).
  - Duyệt từng bước thủ công (**Bước sau** / **Bước trước**).
  - Thanh trượt điều chỉnh tốc độ mô phỏng từ `100ms` đến `2000ms`.
- **Log hoạt động chi tiết**:
  - Biểu diễn trạng thái bàn cờ dạng ký tự tại mỗi bước.
  - Hiển thị hướng di chuyển của ô trống `_`: **U** (Lên - Up), **D** (Xuống - Down), **L** (Trái - Left), **R** (Phải - Right).
  - Hiển thị các thông số chi tiết của từng bước theo thuật toán đã chọn như: Chi phí thực tế $g(n)$, Heuristic $h(n)$, Giá trị hàm đánh giá $f(n)$, Độ sâu (Depth), Ngưỡng thử (Threshold).
  - In ra chuỗi nước đi hoàn chỉnh sau khi kết thúc tìm kiếm.

---

## Yêu cầu hệ thống

Ứng dụng chỉ sử dụng các thư viện chuẩn (Built-in standard libraries) của Python, **không cần cài đặt thêm bất kỳ thư viện ngoài nào (no pip required)**:
- **Python 3.x**
- Các module tích hợp sẵn: `tkinter`, `random`, `queue`, `heapq`, `threading`.

---

## Hướng dẫn chạy ứng dụng

1. Mở terminal tại thư mục chứa file mã nguồn.
2. Chạy lệnh sau để khởi động ứng dụng:
   ```bash
   python 24162039_NguyenDucHoc_8puzzle_Visualize.py
   ```

---

## Hướng dẫn sử dụng

1. **Bước 1**: Nhấn nút **"Sinh ma trận ngẫu nhiên"** để tạo một trạng thái bắt đầu mới ngẫu nhiên (hoặc dùng trạng thái mặc định ban đầu của ứng dụng).
2. **Bước 2**: Trong mục **"Chọn Thuật Toán"**, click vào thuật toán bạn muốn chạy. Giao diện sẽ hiển thị trạng thái tìm kiếm và tự động cập nhật kết quả khi tìm thấy.
3. **Bước 3**: 
   - Sử dụng **"Bước trước"** / **"Bước sau"** để quan sát từng bước di chuyển thủ công.
   - Nhấn **"Tự động chạy"** để xem mô phỏng chuyển động tự động. Bạn có thể kéo thanh trượt **Tốc độ chạy** để thay đổi thời gian chờ giữa các bước.
   - Nhấn **"Xóa log"** để làm sạch vùng hiển thị lịch sử di chuyển bất cứ lúc nào.