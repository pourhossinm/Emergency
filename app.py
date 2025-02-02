from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
    return render_template("form.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # مقدار پیش‌فرض 5000 است، اگر PORT موجود نباشد
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
