# Mobile Shop Flask AI WebApp - phiên bản giao diện sản phẩm nâng cấp

## Đã nâng cấp
- Ảnh sản phẩm thật/ảnh sản phẩm tham khảo thay cho icon điện thoại.
- Card sản phẩm: ảnh, tên, hãng, sao đánh giá, số đánh giá, giá cũ, giá mới, % giảm, nút thêm giỏ.
- Trang chi tiết: ảnh lớn, % giảm, thông số kỹ thuật dạng danh sách, mô tả, tồn kho, lợi ích mua hàng.
- Khu vực đánh giá khách hàng.
- Khu vực AI tư vấn ngay trên trang chi tiết.
- Sản phẩm tương tự vẫn hoạt động.
- Seed dữ liệu tự cập nhật ảnh cho database cũ, không cần xóa database.
- Chatbot vẫn hoạt động theo ngân sách/camera/gaming.

## Chạy dự án

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Mở: http://127.0.0.1:5000

Admin:
- Email: admin@mobileshop.vn
- Password: admin123

## Lưu ý về ảnh
Các URL ảnh demo trong `app.py` trỏ tới ảnh sản phẩm từ các trang bán lẻ/nhà sản xuất. Khi làm đồ án hoặc triển khai công khai, nên thay bằng ảnh bạn có quyền sử dụng và lưu tại `static/images/` để website không phụ thuộc internet.
