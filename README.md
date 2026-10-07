#  Mobile Shop Flask AI WebApp

Website quản lý bán hàng điện thoại **Mobile Shop** được xây dựng bằng **Python **, tích hợp **AI Chatbot hỗ trợ tư vấn khách hàng**.

##  Giới thiệu

Mobile Shop cung cấp nền tảng bán điện thoại trực tuyến với giao diện hiện đại, hỗ trợ khách hàng tìm kiếm, xem thông tin sản phẩm, quản lý giỏ hàng và đặt hàng.

Hệ thống đồng thời cung cấp trang quản trị dành cho Admin để quản lý sản phẩm, đơn hàng, khách hàng và doanh thu.

##  Chức năng chính

### Khách hàng

- Đăng ký tài khoản
- Đăng nhập / đăng xuất
- Xem danh sách sản phẩm
- Tìm kiếm sản phẩm
- Lọc sản phẩm theo hãng và giá
- Sắp xếp sản phẩm
- Xem sản phẩm nổi bật
- Xem sản phẩm khuyến mãi
- Xem chi tiết sản phẩm
- Thêm sản phẩm vào giỏ hàng
- Đặt hàng
- Xem thông tin tài khoản
- Xem lịch sử mua hàng
- Đánh giá sản phẩm

### Giao diện sản phẩm

Mỗi sản phẩm hiển thị:

- Ảnh sản phẩm thật
- Tên sản phẩm
- Hãng sản xuất
- Điểm đánh giá
- Số lượng đánh giá
- Giá cũ
- Giá mới
- Phần trăm giảm giá
- Tình trạng tồn kho
- Nút **Thêm vào giỏ**

###  Trang chi tiết sản phẩm

Trang chi tiết bao gồm:

- Ảnh sản phẩm kích thước lớn
- Tên sản phẩm
- Giá bán
- Giá cũ
- Phần trăm giảm
- Thông số kỹ thuật
- Mô tả sản phẩm
- Tình trạng tồn kho
- Chính sách / lợi ích mua hàng
- Đánh giá khách hàng
- Sản phẩm tương tự
- AI tư vấn sản phẩm

###  AI Chatbot

AI Chatbot hỗ trợ khách hàng lựa chọn điện thoại dựa trên:

-  Ngân sách
-  Nhu cầu camera
-  Nhu cầu chơi game
-  Thời lượng pin
-  Hãng điện thoại
-  Nhu cầu sử dụng

###  Ví dụ kiểm thử AI Chatbot

#### Test 1 – Tư vấn theo ngân sách
> "Tôi có ngân sách 8 triệu, hãy tư vấn cho tôi một chiếc điện thoại phù hợp."

**Mục tiêu:** Kiểm tra khả năng đề xuất sản phẩm theo mức giá.

#### Test 2 – Tư vấn camera
> "Tôi cần điện thoại chụp ảnh đẹp, đặc biệt là chụp ảnh ban đêm. Nên chọn máy nào?"

**Mục tiêu:** Kiểm tra khả năng tư vấn theo nhu cầu camera.

#### Test 3 – Tư vấn chơi game
> "Tôi cần điện thoại khoảng 12 triệu để chơi PUBG và Liên Quân, hãy tư vấn giúp tôi."

**Mục tiêu:** Kiểm tra khả năng lựa chọn điện thoại phục vụ gaming.

#### Test 4 – Tư vấn thời lượng pin
> "Tôi thường xuyên sử dụng điện thoại cả ngày, hãy tư vấn cho tôi máy có pin tốt."

**Mục tiêu:** Kiểm tra khả năng tư vấn theo nhu cầu sử dụng và thời lượng pin.

#### Test 5 – Tư vấn theo hãng
> "Tôi muốn mua điện thoại Samsung trong khoảng giá 15 triệu. Bạn tư vấn giúp tôi."

**Mục tiêu:** Kiểm tra khả năng lọc và tư vấn sản phẩm theo thương hiệu.

#### Test 6 – Kết hợp nhiều tiêu chí
> "Tôi có 15 triệu, muốn điện thoại Samsung, camera đẹp và pin tốt. Có sản phẩm nào phù hợp không?"

**Mục tiêu:** Kiểm tra khả năng xử lý nhiều yêu cầu cùng lúc.

#### Test 7 – Tư vấn cho sinh viên
> "Tôi là sinh viên, ngân sách khoảng 7 triệu, cần điện thoại học tập, xem YouTube và chơi game nhẹ."

**Mục tiêu:** Kiểm tra khả năng tư vấn theo đối tượng và nhu cầu sử dụng.

#### Test 8 – So sánh sản phẩm
> "Hãy tư vấn giúp tôi nên chọn iPhone hay Samsung trong tầm giá 20 triệu."

**Mục tiêu:** Kiểm tra khả năng phân tích và đưa ra lựa chọn giữa các thương hiệu.

#### Test 9 – Tìm điện thoại chơi game cao cấp
> "Tôi có ngân sách 20 triệu và ưu tiên hiệu năng chơi game. Hãy tìm cho tôi sản phẩm phù hợp."

**Mục tiêu:** Kiểm tra khả năng ưu tiên hiệu năng và ngân sách.

#### Test 10 – Tư vấn tổng hợp
> "Tôi có khoảng 18 triệu, cần điện thoại chụp ảnh đẹp, chơi game tốt, pin ổn và muốn mua Samsung hoặc iPhone."

**Mục tiêu:** Kiểm tra khả năng xử lý nhiều tiêu chí và đề xuất sản phẩm phù hợp.

##  Chức năng Admin

Admin có thể quản lý:

###  Dashboard

- Tổng số sản phẩm
- Tổng số khách hàng
- Tổng số đơn hàng
- Doanh thu
- Thống kê bán hàng
- Doanh thu theo hãng

###  Quản lý sản phẩm

- Xem danh sách sản phẩm
- Thêm sản phẩm
- Sửa sản phẩm
- Xóa sản phẩm
- Tìm kiếm sản phẩm
- Lọc sản phẩm

###  Quản lý đơn hàng

- Xem danh sách đơn hàng
- Tìm kiếm đơn hàng
- Lọc đơn hàng
- Duyệt đơn hàng
- Hủy đơn hàng
- Theo dõi trạng thái đơn hàng

###  Quản lý khách hàng

- Xem danh sách khách hàng
- Tìm kiếm khách hàng
- Xem thông tin khách hàng
- Khóa tài khoản
- Quản lý tài khoản khách hàng

##  Dữ liệu và hình ảnh sản phẩm

- Sử dụng hình ảnh sản phẩm thực tế/tham khảo.
- Dữ liệu sản phẩm được seed tự động.
- Có thể cập nhật hình ảnh cho database hiện tại.
- Không cần xóa database cũ khi cập nhật dữ liệu.

##  Công nghệ sử dụng

- **Python**
- **Flask**
- **HTML5**
- **CSS3**
- **JavaScript**
- **SQLite**
- **Jinja2**
- **AI Chatbot**
- **Git / GitHub**

##  Cấu trúc project

```text
Mobile_Shop_Flask_AI_WebApp_Pro/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── admin/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── product_detail.html
│   ├── cart.html
│   ├── checkout.html
│   └── orders.html
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore