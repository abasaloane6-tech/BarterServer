from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = "1234"

# قائمة المنتجات
products = []

# بيانات المدير
ADMIN = "abas"
PASSWORD = "1234"

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("home.html", products=products)

# صفحة رفع إعلان جديد
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        desc = request.form["desc"]
        whatsapp = request.form["whatsapp"]

        # رفع صورة المنتج
        file = request.files["image"]
        filename = file.filename
        path = os.path.join("static", filename)
        file.save(path)

        # إضافة المنتج للقائمة
        products.append({
            "name": name,
            "price": price,
            "desc": desc,
            "whatsapp": whatsapp,
            "image": filename
        })

        return redirect("/")

    return render_template("add.html")

# لوحة تحكم المدير
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["user"]
        pw = request.form["pw"]
        if user == ADMIN and pw == PASSWORD:
            session["admin"] = True

    if "admin" in session:
        return render_template("admin.html", products=products)
    return render_template("login.html")

# حذف إعلان
@app.route("/delete/<int:i>")
def delete(i):
    if "admin" in session:
        products.pop(i)
    return redirect("/admin")

# تشغيل السيرفر
app.run(host="0.0.0.0", port=5000)
