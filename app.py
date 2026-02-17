from flask import Flask, render_template, request, redirect, session
import os, json

app = Flask(__name__)
app.secret_key = "1234"

# منع الكاش
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

# ملفات حفظ البيانات
DATA_FILE = "products.json"
CHAT_FILE = "chat.json"
BANNER_FILE = "banner.json"

# تحميل المنتجات
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        products = json.load(f)
else:
    products = []

# تحميل الدردشة
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        chat_messages = json.load(f)
else:
    chat_messages = []

# تحميل البنر
if os.path.exists(BANNER_FILE):
    with open(BANNER_FILE, "r", encoding="utf-8") as f:
        banner = json.load(f)
else:
    banner = {"image": "default-banner.jpg"}  # ضع هذه الصورة في static/

# بيانات المدير
ADMIN = "abas"
PASSWORD = "1234"

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("home.html", products=products, banner=banner)

# صفحة رفع البنر
@app.route("/banner", methods=["GET","POST"])
def banner_page():
    global banner
    if request.method == "POST":
        file = request.files["banner_image"]
        filename = file.filename
        path = os.path.join("static", filename)
        file.save(path)
        banner["image"] = filename
        with open(BANNER_FILE, "w", encoding="utf-8") as f:
            json.dump(banner, f, ensure_ascii=False, indent=4)
        return redirect("/banner")
    return render_template("banner.html", banner=banner)

# إضافة إعلان / منتج
@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        desc = request.form.get("desc","")
        price = request.form["price"]
        whatsapp = request.form["whatsapp"]
        file = request.files["image"]
        filename = file.filename
        path = os.path.join("static", filename)
        file.save(path)

        products.append({
            "name": name,
            "desc": desc,
            "price": price,
            "whatsapp": whatsapp,
            "image": filename
        })

        with open(DATA_FILE,"w", encoding="utf-8") as f:
            json.dump(products,f, ensure_ascii=False, indent=4)
        return redirect("/")
    return render_template("add.html")

# لوحة المدير
@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        user = request.form["user"]
        pw = request.form["pw"]
        if user == ADMIN and pw == PASSWORD:
            session["admin"] = True

    if "admin" in session:
        return render_template("admin.html", products=products, banner=banner)
    return render_template("login.html")

# حذف إعلان + الصورة
@app.route("/delete/<int:i>")
def delete(i):
    if "admin" in session:
        # حذف الصورة من السيرفر
        img = products[i]["image"]
        img_path = os.path.join("static", img)
        if os.path.exists(img_path):
            os.remove(img_path)
        # حذف المنتج
        products.pop(i)
        with open(DATA_FILE,"w", encoding="utf-8") as f:
            json.dump(products,f, ensure_ascii=False, indent=4)
    return redirect("/admin")

# الدردشة
@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "POST":
        username = request.form["username"]
        message = request.form["message"]
        chat_messages.append({"username":username,"message":message})
        with open(CHAT_FILE,"w", encoding="utf-8") as f:
            json.dump(chat_messages,f, ensure_ascii=False, indent=4)
        return redirect("/chat")
    return render_template("chat.html", chat_messages=chat_messages)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
