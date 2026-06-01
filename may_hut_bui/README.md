# HƯỚNG DẪN CHẠY CODE MÁY HÚT BỤI (MODEL-BASED)

## 1. Giới thiệu
Đây là bài tập mô phỏng Tác nhân phản xạ dựa trên mô hình (Model-based Reflex Agent).
Robot không chỉ nhìn rồi làm, mà nó còn lưu trạng thái môi trường vào một biến 
gọi là `bo_nho_ban_do`.

## 2. Cách xử lý vật cản
Trong code này, mình có thêm biến `co_vat_can`. 
- Nếu cảm biến báo `True`: Robot sẽ không thực hiện lệnh di chuyển thông thường 
  (vì sẽ đâm vào tường/vật cản).
- Thay vào đó, nó sẽ kích hoạt luật "Quay đầu" hoặc tìm đường khác dựa trên 
  thông tin đã lưu.

## 3. Cách chạy
- Cài đặt Python 3.x
- Mở terminal và gõ: python robot_ai.py
- Có thể sửa các thông số trong phần trong chương trình để test các trường hợp khác nhau.

## 4. Hạn chế
- Hiện tại code mới chỉ mô phỏng 2 phòng A và B.
- Vật cản mới chỉ dừng lại ở việc báo hiệu chứ chưa có thuật toán tìm đường (A*) phức tạp.