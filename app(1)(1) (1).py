from flask import Flask, request, render_template_string
import re
import validators

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>ICT Website Security Checker & Password Detector</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#0f172a;color:white;}
.card{background:#1e293b;border-radius:15px;}
</style>
</head>
<body>
<div class="container mt-4">
<h1 class="text-center">ICT Website Security Checker & Password Detector</h1>
<p class="text-center">
Muhammad Shahbaz Malik (25-ME-151)<br>
Muhammad Sameer Niaz (25-ME-151)<br>
Zain Abbas (25-ME-159)
</p>

<div class="card p-4 mb-3">
<h3>Website Security Checker</h3>
<form method="post">
<input name="website" class="form-control" placeholder="https://example.com">
<button class="btn btn-info mt-2">Check</button>
</form>
{% if website_result %}<p class="mt-3">{{website_result}}</p>{% endif %}
</div>

<div class="card p-4">
<h3>Password Detector</h3>
<form method="post">
<input type="password" name="password" class="form-control" placeholder="Password">
<button class="btn btn-success mt-2">Analyze</button>
</form>
{% if strength %}
<p class="mt-3"><b>{{strength}}</b></p>
<p>{{message}}</p>
{% endif %}
</div>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    website_result = None
    strength = None
    message = None

    if request.method == "POST":
        website = request.form.get("website")
        password = request.form.get("password")

        if website:
            if validators.url(website):
                website_result = "Secure HTTPS Website" if website.startswith("https://") else "Website not using HTTPS"
            else:
                website_result = "Invalid URL"

        if password:
            score = 0
            if len(password) >= 8: score += 20
            if re.search(r"[A-Z]", password): score += 20
            if re.search(r"[a-z]", password): score += 20
            if re.search(r"\d", password): score += 20
            if re.search(r"[!@#$%^&*()]", password): score += 20

            if score <= 40:
                strength = "Weak Password"
            elif score <= 80:
                strength = "Medium Password"
            else:
                strength = "Strong Password"
            message = f"Score: {score}/100"

    return render_template_string(HTML, website_result=website_result, strength=strength, message=message)

if __name__ == "__main__":
    app.run(debug=True)
