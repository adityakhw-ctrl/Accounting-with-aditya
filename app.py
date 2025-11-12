# MADE BY ADITYA 💎
from flask import Flask, render_template, request, redirect, url_for, session
import webbrowser as _wb, time as _tm, os as _o

app = Flask(__name__)
app.secret_key = "aditya@7357_secure_key"

# Simple subscription-checking stub for demo: in production replace with DB/webhook checks
AUTHORIZED_USERS = {"demo@local": True}  # placeholder

def require_auth(f):
    from functools import wraps
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("user_email") or not AUTHORIZED_USERS.get(session.get("user_email")):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        # For demo purpose: accept login if email in AUTHORIZED_USERS
        if email:
            session["user_email"] = email
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
@require_auth
def home():
    return render_template("home.html")

@app.route("/company")
@require_auth
def company():
    company_data = {
        "name": "Demo Tally Pvt. Ltd.",
        "entries": 1254,
        "balance": "₹ 5,74,230",
        "daybook": "42 entries today"
    }
    return render_template("company.html", data=company_data)

@app.route("/entry")
@require_auth
def entry():
    return render_template("entry.html")

@app.route("/gstr")
@require_auth
def gstr():
    return render_template("gstr.html")

# Minimal webhook endpoint for payment gateways (to be secured in production)
@app.route("/payment_webhook", methods=["POST"])
def payment_webhook():
    # Example: gateway will POST JSON {"email":"user@example.com","plan":"monthly"}
    from flask import request, jsonify
    data = request.get_json() or {}
    email = data.get("email")
    if not email:
        return jsonify({"ok": False, "error": "no email"}), 400
    # Grant access (in production validate gateway signature)
    AUTHORIZED_USERS[email] = True
    return jsonify({"ok": True})

if __name__ == "__main__":
    print("Starting Flask dashboard...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
