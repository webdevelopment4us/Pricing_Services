from flask import Flask, Blueprint, render_template
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config.update(
    ADMIN=os.environ.get("ADMIN")
)

@app.route("/")
def home():
    return render_template("home.html")

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")








