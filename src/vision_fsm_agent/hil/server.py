"""
Human-in-the-Loop (HIL) correction server (Flask).

A lightweight HTTP service that brokers manual corrections between a human
operator and a running agent. The agent polls this server for corrections;
the operator (or a test script) pushes corrections via POST.

API endpoints (all under ``/hil``):

    GET  /hil/get_correction   - Pop the next pending correction (or ``none``)
    POST /hil/set_correction   - Push a correction for the agent to apply
    POST /hil/send_correction  - Record a correction as learning data
    POST /hil/send_status      - Record an agent status report
    POST /hil/get_decision     - (Stub) return a decision for learning data
    GET  /hil/status           - Server health and counters

Run standalone::

    python -m src.hil_server
    # or: python run.py --hil

Safety note
-----------
This server is intended for local, controlled demo / research environments.
It binds to ``0.0.0.0`` by default for convenience on a LAN, but you should
restrict access (firewall / reverse proxy) in any shared environment.
"""

from __future__ import annotations

import logging
import time

from flask import Flask, jsonify, request

logger = logging.getLogger("HilServer")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - HilServer - %(levelname)s - %(message)s",
)

app = Flask(__name__)

# In-memory stores. Suitable for a single-process demo server.
correction_store: dict = {
    "last_correction": None,
    "correction_history": [],
}

learning_store: dict = {
    "learning_history": [],
    "status_history": [],
}

_MAX_HISTORY = 100


def _trim(lst: list, limit: int = _MAX_HISTORY // 2) -> None:
    """Keep a list bounded."""
    if len(lst) > limit * 2:
        del lst[: len(lst) - limit]


@app.route("/hil/get_correction", methods=["GET"])
def get_correction():
    """Pop the next pending correction.

    Returns the stored correction and clears it (one-shot semantics),
    or ``{"type": "none"}`` if nothing is pending.
    """
    try:
        correction = correction_store.get("last_correction")
        if correction:
            logger.info("Returning correction: %s", correction)
            correction_store["last_correction"] = None
            return jsonify(correction), 200
        return jsonify({"type": "none", "message": "no correction pending"}), 200
    except Exception as exc:  # pragma: no cover
        logger.error("get_correction error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/hil/set_correction", methods=["POST"])
def set_correction():
    """Push a correction for the agent to consume on its next poll."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "missing JSON body"}), 400
        required = ["type", "action", "correct_params"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"missing field: {field}"}), 400
        correction_store["last_correction"] = data
        correction_store["correction_history"].append(
            {"correction": data, "timestamp": time.time()}
        )
        _trim(correction_store["correction_history"])
        logger.info("Correction set: %s", data)
        return jsonify({"status": "success", "message": "correction stored"}), 200
    except Exception as exc:  # pragma: no cover
        logger.error("set_correction error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/hil/send_correction", methods=["POST"])
def send_correction():
    """Record a correction as learning data (agent -> server)."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "missing JSON body"}), 400
        learning_store["learning_history"].append({"data": data, "received_at": time.time()})
        _trim(learning_store["learning_history"])
        logger.info("Learning data recorded")
        return jsonify({"status": "success", "message": "learning data recorded"}), 200
    except Exception as exc:  # pragma: no cover
        logger.error("send_correction error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/hil/send_status", methods=["POST"])
def send_status():
    """Record an agent status report."""
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "missing JSON body"}), 400
        learning_store["status_history"].append({"data": data, "received_at": time.time()})
        _trim(learning_store["status_history"])
        return jsonify({"status": "success", "message": "status recorded"}), 200
    except Exception as exc:  # pragma: no cover
        logger.error("send_status error: %s", exc)
        return jsonify({"error": str(exc)}), 500


@app.route("/hil/get_decision", methods=["POST"])
def get_decision():
    """Stub decision endpoint.

    In a real deployment this could consult recorded learning data or an
    external model. Here it simply echoes back a conservative "continue"
    decision so the agent loop keeps running.
    """
    return (
        jsonify(
            {
                "action": "continue",
                "reason": "no learned policy yet; continue autonomously",
            }
        ),
        200,
    )


@app.route("/hil/status", methods=["GET"])
def status():
    """Server health and counters."""
    return (
        jsonify(
            {
                "status": "running",
                "timestamp": time.time(),
                "correction_count": len(correction_store["correction_history"]),
                "learning_count": len(learning_store["learning_history"]),
                "status_count": len(learning_store["status_history"]),
                "has_pending_correction": correction_store["last_correction"] is not None,
            }
        ),
        200,
    )


@app.route("/hil/reset", methods=["POST"])
def reset():
    """Clear all in-memory stores (useful for tests)."""
    correction_store["last_correction"] = None
    correction_store["correction_history"].clear()
    learning_store["learning_history"].clear()
    learning_store["status_history"].clear()
    return jsonify({"status": "success", "message": "stores cleared"}), 200


def run(host: str = "0.0.0.0", port: int = 8001) -> None:
    """Start the HIL server (blocking)."""
    logger.info("HIL server starting on http://%s:%d/hil", host, port)
    logger.info("Endpoints:")
    logger.info("  GET  /hil/get_correction")
    logger.info("  POST /hil/set_correction")
    logger.info("  POST /hil/send_correction")
    logger.info("  POST /hil/send_status")
    logger.info("  POST /hil/get_decision")
    logger.info("  GET  /hil/status")
    logger.info("  POST /hil/reset")
    app.run(host=host, port=port, debug=False, threaded=True)


if __name__ == "__main__":  # pragma: no cover
    run()
