from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, func

app = Flask(__name__)
app.config["SECRET_KEY"] = "mobile-shop-dev-secret-change-me"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mobile_shop.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer")
    is_locked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship("Order", backref="customer", lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    old_price = db.Column(db.Integer)
    image = db.Column(db.String(500), default="")
    description = db.Column(db.Text, default="")
    specs = db.Column(db.Text, default="")
    rating = db.Column(db.Float, default=5.0)
    reviews = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    is_sale = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship("OrderItem", backref="product", lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    receiver_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    payment_method = db.Column(db.String(40), default="COD")
    status = db.Column(db.String(30), default="pending")
    total = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

def current_user():
    uid = session.get("user_id")
    return db.session.get(User, uid) if uid else None

@app.context_processor
def inject_globals():
    cart = session.get("cart", {})
    cart_count = sum(cart.values())
    return {"current_user": current_user(), "cart_count": cart_count}

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Vui lòng đăng nhập để tiếp tục.", "warning")
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or user.role != "admin":
            flash("Bạn không có quyền truy cập khu vực quản trị.", "danger")
            return redirect(url_for("home"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    featured = Product.query.filter_by(is_featured=True).limit(8).all()
    newest = Product.query.filter_by(is_new=True).order_by(Product.created_at.desc()).limit(8).all()
    sale = Product.query.filter_by(is_sale=True).limit(8).all()
    return render_template("home.html", featured=featured, newest=newest, sale=sale)

@app.route("/products")
def products():
    q = request.args.get("q", "").strip()
    brand = request.args.get("brand", "").strip()
    min_price = request.args.get("min_price", type=int)
    max_price = request.args.get("max_price", type=int)
    sort = request.args.get("sort", "newest")
    query = Product.query
    if q:
        query = query.filter(or_(Product.name.ilike(f"%{q}%"), Product.brand.ilike(f"%{q}%")))
    if brand:
        query = query.filter_by(brand=brand)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())
    items = query.all()
    brands = [x[0] for x in db.session.query(Product.brand).distinct().order_by(Product.brand).all()]
    return render_template("products.html", products=items, brands=brands)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    related = Product.query.filter(Product.brand == product.brand, Product.id != product.id).limit(4).all()
    if len(related) < 4:
        extra = Product.query.filter(Product.id != product.id).limit(4).all()
        seen = {p.id for p in related}
        related += [p for p in extra if p.id not in seen][:4-len(related)]
    return render_template("product_detail.html", product=product, related=related)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["full_name"].strip()
        email = request.form["email"].strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            flash("Email đã tồn tại.", "danger")
            return redirect(url_for("register"))
        user = User(full_name=name, email=email, phone=phone,
                    password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash("Đăng ký thành công. Hãy đăng nhập.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Email hoặc mật khẩu không đúng.", "danger")
            return redirect(url_for("login"))
        if user.is_locked:
            flash("Tài khoản đang bị khóa.", "danger")
            return redirect(url_for("login"))
        session["user_id"] = user.id
        flash("Đăng nhập thành công.", "success")
        return redirect(request.args.get("next") or url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for("home"))

def get_cart_items():
    cart = session.get("cart", {})
    result = []
    total = 0
    for pid, qty in cart.items():
        product = db.session.get(Product, int(pid))
        if product and qty > 0:
            subtotal = product.price * qty
            result.append((product, qty, subtotal))
            total += subtotal
    return result, total

@app.route("/cart")
def cart():
    items, total = get_cart_items()
    return render_template("cart.html", items=items, total=total)

@app.post("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    product = db.get_or_404(Product, product_id)
    cart = session.get("cart", {})
    key = str(product_id)
    new_qty = cart.get(key, 0) + max(1, request.form.get("quantity", 1, type=int))
    if new_qty > product.stock:
        flash("Số lượng vượt quá tồn kho.", "warning")
    else:
        cart[key] = new_qty
        session["cart"] = cart
        flash(f"Đã thêm {product.name} vào giỏ hàng.", "success")
    return redirect(request.referrer or url_for("products"))

@app.post("/cart/update")
def update_cart():
    cart = session.get("cart", {})
    for key in list(cart.keys()):
        qty = request.form.get(f"qty_{key}", type=int)
        product = db.session.get(Product, int(key))
        if not product or not qty or qty < 1:
            cart.pop(key, None)
        else:
            cart[key] = min(qty, product.stock)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.get("/cart/remove/<int:product_id>")
def remove_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("cart"))

@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items, total = get_cart_items()
    if not items:
        flash("Giỏ hàng đang trống.", "warning")
        return redirect(url_for("products"))
    if request.method == "POST":
        user = current_user()
        order = Order(
            user_id=user.id,
            receiver_name=request.form["receiver_name"].strip(),
            phone=request.form["phone"].strip(),
            address=request.form["address"].strip(),
            payment_method=request.form.get("payment_method", "COD"),
            total=total
        )
        db.session.add(order)
        for product, qty, subtotal in items:
            if qty > product.stock:
                flash(f"Sản phẩm {product.name} không đủ tồn kho.", "danger")
                db.session.rollback()
                return redirect(url_for("cart"))
            product.stock -= qty
            db.session.add(OrderItem(order=order, product_id=product.id, quantity=qty, price=product.price))
        db.session.commit()
        session["cart"] = {}
        flash(f"Đặt hàng thành công! Mã đơn #{order.id}.", "success")
        return redirect(url_for("orders"))
    return render_template("checkout.html", items=items, total=total)

@app.route("/account")
@login_required
def account():
    return render_template("account.html", orders=Order.query.filter_by(user_id=current_user().id).order_by(Order.created_at.desc()).all())

@app.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user().id).order_by(Order.created_at.desc()).all()
    return render_template("orders.html", orders=orders)

# ---------- Admin ----------
@app.route("/admin")
@admin_required
def admin_dashboard():
    revenue = db.session.query(func.coalesce(func.sum(Order.total), 0)).filter(Order.status != "cancelled").scalar()
    order_count = Order.query.count()
    customer_count = User.query.filter_by(role="customer").count()
    product_count = Product.query.count()
    brand_stats = db.session.query(
        Product.brand,
        func.coalesce(func.sum(OrderItem.quantity), 0).label("qty"),
        func.coalesce(func.sum(OrderItem.quantity * OrderItem.price), 0).label("revenue")
    ).join(OrderItem, Product.id == OrderItem.product_id).join(Order, Order.id == OrderItem.order_id).filter(Order.status != "cancelled").group_by(Product.brand).order_by(func.sum(OrderItem.quantity * OrderItem.price).desc()).all()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(8).all()
    return render_template("admin/dashboard.html", revenue=revenue, order_count=order_count,
                           customer_count=customer_count, product_count=product_count,
                           brand_stats=brand_stats, recent_orders=recent_orders)

@app.route("/admin/products", methods=["GET", "POST"])
@admin_required
def admin_products():
    if request.method == "POST":
        p = Product(
            name=request.form["name"].strip(), brand=request.form["brand"].strip(),
            price=request.form.get("price", type=int) or 0, old_price=request.form.get("old_price", type=int),
            image=request.form.get("image", "").strip(), description=request.form.get("description", ""),
            specs=request.form.get("specs", ""), rating=request.form.get("rating", type=float) or 5,
            stock=request.form.get("stock", type=int) or 0,
            is_featured="is_featured" in request.form, is_new="is_new" in request.form, is_sale="is_sale" in request.form
        )
        db.session.add(p)
        db.session.commit()
        flash("Đã thêm sản phẩm.", "success")
        return redirect(url_for("admin_products"))
    q = request.args.get("q", "").strip()
    query = Product.query
    if q:
        query = query.filter(or_(Product.name.ilike(f"%{q}%"), Product.brand.ilike(f"%{q}%")))
    return render_template("admin/products.html", products=query.order_by(Product.id.desc()).all())

@app.post("/admin/products/delete/<int:product_id>")
@admin_required
def admin_product_delete(product_id):
    p = db.get_or_404(Product, product_id)
    if p.order_items:
        flash("Không thể xóa sản phẩm đã có trong đơn hàng. Hãy để tồn kho về 0 hoặc chỉnh sửa sản phẩm.", "warning")
    else:
        db.session.delete(p)
        db.session.commit()
        flash("Đã xóa sản phẩm.", "success")
    return redirect(url_for("admin_products"))

@app.route("/admin/orders")
@admin_required
def admin_orders():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()
    query = Order.query
    if q and q.isdigit():
        query = query.filter(Order.id == int(q))
    if status:
        query = query.filter_by(status=status)
    return render_template("admin/orders.html", orders=query.order_by(Order.created_at.desc()).all())

@app.post("/admin/orders/<int:order_id>/status")
@admin_required
def admin_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    new_status = request.form["status"]
    allowed = {"pending", "confirmed", "shipping", "completed", "cancelled"}
    if new_status not in allowed:
        flash("Trạng thái không hợp lệ.", "danger")
    else:
        if order.status != "cancelled" and new_status == "cancelled":
            for item in order.items:
                item.product.stock += item.quantity
        order.status = new_status
        db.session.commit()
        flash("Đã cập nhật trạng thái đơn hàng.", "success")
    return redirect(url_for("admin_orders"))

@app.route("/admin/customers")
@admin_required
def admin_customers():
    q = request.args.get("q", "").strip()
    query = User.query.filter_by(role="customer")
    if q:
        query = query.filter(or_(User.full_name.ilike(f"%{q}%"), User.email.ilike(f"%{q}%"), User.phone.ilike(f"%{q}%")))
    return render_template("admin/customers.html", customers=query.order_by(User.id.desc()).all())

@app.post("/admin/customers/<int:user_id>/toggle")
@admin_required
def admin_customer_toggle(user_id):
    user = db.get_or_404(User, user_id)
    user.is_locked = not user.is_locked
    db.session.commit()
    flash("Đã cập nhật trạng thái tài khoản.", "success")
    return redirect(url_for("admin_customers"))

# ---------- AI chatbot ----------
@app.post("/api/chat")
def chat_api():
    message = request.json.get("message", "").lower().strip()
    products = Product.query.all()
    budget = None
    import re
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(triệu|tr)", message)
    if m:
        budget = int(float(m.group(1).replace(",", ".")) * 1_000_000)
    if any(k in message for k in ["game", "chơi game", "gaming"]):
        candidates = sorted(products, key=lambda p: (p.rating, p.price), reverse=True)[:3]
        intro = "Nếu bạn ưu tiên chơi game, mình đề xuất các máy có cấu hình mạnh:"
    elif any(k in message for k in ["ảnh", "camera", "chụp"]):
        candidates = sorted(products, key=lambda p: p.rating, reverse=True)[:3]
        intro = "Nếu ưu tiên camera, bạn có thể tham khảo:"
    elif budget:
        candidates = [p for p in products if p.price <= budget and p.stock > 0]
        candidates = sorted(candidates, key=lambda p: p.rating, reverse=True)[:3]
        intro = f"Với ngân sách khoảng {budget:,.0f} VNĐ, mình gợi ý:"
    else:
        candidates = sorted(products, key=lambda p: (p.is_featured, p.rating), reverse=True)[:3]
        intro = "Mình có thể tư vấn theo ngân sách, camera, gaming hoặc nhu cầu sử dụng. Bạn có thể tham khảo:"
    if not candidates:
        return jsonify({"reply": "Mình chưa tìm thấy sản phẩm phù hợp. Bạn thử tăng ngân sách hoặc nói rõ nhu cầu nhé."})
    cards = [{"id": p.id, "name": p.name, "price": p.price, "rating": p.rating} for p in candidates]
    return jsonify({"reply": intro, "products": cards})

def seed():
    db.create_all()

    if not User.query.filter_by(email="admin@mobileshop.vn").first():
        db.session.add(User(
            full_name="Quản trị viên", email="admin@mobileshop.vn",
            phone="0900000000", password_hash=generate_password_hash("admin123"),
            role="admin"
        ))

    # Ảnh sản phẩm thật từ các trang bán lẻ/nhà sản xuất dùng cho bản demo đồ án.
    # Có thể thay bằng ảnh riêng của cửa hàng trong trường image.
    data = [
        ("iPhone 15", "Apple", 18990000, 20990000,
         "https://cdn.tgdd.vn/Products/Images/42/281570/iphone-15-1-3.jpg",
         "iPhone 15 – thiết kế hiện đại, hiệu năng mạnh.",
         "A16 Bionic; OLED 6.1 inch; Camera chính 48MP; 128GB; 5G",
         4.8, 120, 32, True, True, True),

        ("iPhone 15 Pro Max", "Apple", 29990000, 32990000,
         "https://cdn.tgdd.vn/Products/Images/42/305660/iphone-15-pro-max-white-1.jpg",
         "Flagship cao cấp với khung Titan và camera chuyên nghiệp.",
         "A17 Pro; OLED 6.7 inch; Camera 48MP; 256GB; ProMotion 120Hz",
         4.9, 120, 12, True, False, True),

        ("Galaxy S24", "Samsung", 16990000, 18990000,
         "https://shop.theclub.com.hk/media/catalog/product/cache/bfa0ef71007a70e7a7d022a269485c94/4/2/4225091_1.jpg",
         "Màn hình đẹp, AI thông minh, camera đa năng.",
         "Snapdragon 8 Gen 3; AMOLED 6.2 inch; Camera 50MP; 256GB; 5G",
         4.8, 120, 24, True, True, True),

        ("Galaxy A55 5G", "Samsung", 9990000, 10990000,
         "https://i5.walmartimages.com/seo/Samsung-Galaxy-A55-5G-128GB-8GB-for-Tmobile-Mint-Tello-Global-GSM-Unlocked-No-CDMA-6-6-120Hz-50MP-International-Model-Light-Blue_14af283d-fe08-4a97-a507-e0e5e8f1d21e.6effb1a3e06034aa0653d4399c488d21.jpeg?odnBg=FFFFFF&odnHeight=573&odnWidth=573",
         "Lựa chọn cân bằng cho học tập và giải trí.",
         "Super AMOLED 6.6 inch 120Hz; Camera 50MP; 8GB RAM; 128GB; 5G",
         4.6, 120, 40, False, True, True),

        ("Xiaomi 14", "Xiaomi", 13990000, 15990000,
         "https://shopxiaomi.ie/cdn/shop/files/1027119Xiaomi14512GBWhiteSF_medium.png?v=1752761402",
         "Hiệu năng cao, camera Leica, thiết kế nhỏ gọn.",
         "Snapdragon 8 Gen 3; AMOLED 6.36 inch; Leica 50MP; 512GB; 5G",
         4.7, 120, 28, True, False, True),

        ("Redmi Note 13", "Xiaomi", 5990000, 6990000,
         "https://fdn2.gsmarena.com/vv/pics/xiaomi/xiaomi-redmi-note-13-4g-1.jpg",
         "Giá tốt, pin lớn, phù hợp sinh viên.",
         "AMOLED 6.67 inch 120Hz; Camera 108MP; 5000mAh; 8GB RAM; 256GB",
         4.5, 120, 55, False, True, True),

        ("OPPO Reno12", "OPPO", 9990000, 10990000,
         "https://fdn2.gsmarena.com/vv/pics/oppo/oppo-reno12-1.jpg",
         "Thiết kế đẹp, chân dung AI, phù hợp học tập và giải trí.",
         "AMOLED 6.7 inch 120Hz; Camera 50MP; 5000mAh; 12GB RAM; 256GB",
         4.6, 120, 35, False, True, True),

        ("OPPO Find X8", "OPPO", 21990000, 23990000,
         "https://cdnv2.tgdd.vn/mwg-static/tgdd/Products/Images/42/322128/oppo-find-x8-den-1-638684901443517813.jpg",
         "Flagship camera và hiệu năng mạnh với AI hỗ trợ.",
         "Dimensity 9400; AMOLED 6.59 inch 120Hz; 3 camera 50MP; 5630mAh; 512GB",
         4.8, 120, 15, True, False, True),
    ]

    for name, brand, price, old_price, image, desc, specs, rating, reviews, stock, featured, is_new, sale in data:
        p = Product.query.filter_by(name=name).first()
        if not p:
            p = Product(name=name)
            db.session.add(p)
        p.brand = brand
        p.price = price
        p.old_price = old_price
        p.image = image
        p.description = desc
        p.specs = specs
        p.rating = rating
        p.reviews = reviews
        p.stock = stock
        p.is_featured = featured
        p.is_new = is_new
        p.is_sale = sale

    db.session.commit()

with app.app_context():
    seed()

if __name__ == "__main__":
    app.run(debug=True)
