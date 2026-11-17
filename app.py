"""Điểm khởi động. Chạy: python app.py"""
from flask import Flask, redirect, session, url_for

import config
from blueprints.api.routes import bp as api_bp
from blueprints.auth.routes import bp as auth_bp
from blueprints.operator.routes import bp as operator_bp
from blueprints.student.routes import bp as student_bp
from services import realtime_service


def createApp(startSimulator=True):
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(operator_bp, url_prefix="/operator")
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.context_processor
    def injectGlobals():
        # Các biến này dùng được trong mọi template
        return {
            "BRAND_NAME": config.BRAND_NAME,
            "POLL_INTERVAL_SECONDS": config.POLL_INTERVAL_SECONDS,
            "currentUser": session.get("user"),
        }

    @app.route("/")
    def home():
        user = session.get("user")
        if user and user["role"] == "OPERATOR":
            return redirect(url_for("operator.overview"))
        return redirect(url_for("student.search"))

    if startSimulator and config.SIMULATOR_ENABLED:
        realtime_service.startSimulator()
    return app


if __name__ == "__main__":
    # use_reloader=False để bộ giả lập không bị chạy 2 lần
    createApp().run(host=config.HOST, port=config.PORT, debug=config.DEBUG, use_reloader=False)
