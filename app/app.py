import os
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("checkout-api")

VERSION = "v2.4"

@app.route("/", methods=["GET"])
def index():
    logger.info("Handling request at / endpoint")
    return jsonify({
        "service": "checkout-api",
        "version": VERSION,
        "message": "Release Readiness Demo"
    })

@app.route("/health", methods=["GET"])
def health():
    db_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")
    
    # This endpoint verifies configuration presence, not live dependency connectivity.
    if db_url:
        db_status = "configured"
    else:
        db_status = "missing"
        logger.error("DATABASE_URL is not set; checkout-api is not ready.")

    if redis_url:
        redis_status = "configured"
    else:
        redis_status = "missing"
        logger.error("REDIS_URL is not set; checkout-api is not ready.")

    ready = bool(db_url and redis_url)
    status_code = 200 if ready else 503
    
    return jsonify({
        "status": "ready" if ready else "not_ready",
        "version": VERSION,
        "checks": {
            "database": db_status,
            "redis": redis_status
        }
    }), status_code

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting checkout-api v{VERSION} on port {port}")
    app.run(host="0.0.0.0", port=port)
