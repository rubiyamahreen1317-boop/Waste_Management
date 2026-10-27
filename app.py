import logging
import os

from flask import Flask, jsonify, render_template, request

from controllers.routes import register_routes


def create_app() -> Flask:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

    @app.errorhandler(413)
    def upload_too_large(_error):
        return (
            render_template(
                "error.html",
                title="File is too large",
                message="CSV uploads must be 20 MB or smaller.",
            ),
            413,
        )

    @app.errorhandler(500)
    def internal_error(_error):
        app.logger.exception("Unhandled dashboard error")
        if request.path.startswith("/api/"):
            return jsonify({"error": "The dashboard could not complete that request."}), 500
        return (
            render_template(
                "error.html",
                title="Something went wrong",
                message="The dashboard could not complete that request. Check the app console for details.",
            ),
            500,
        )

    register_routes(app)
    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
