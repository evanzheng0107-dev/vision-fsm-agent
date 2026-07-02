"""
Human-in-the-Loop (HIL) correction client.

The HIL client lets an operator inject manual corrections into a running
agent loop over HTTP. It is the "human" side of human-in-the-loop:

  1. The agent polls ``GET /hil/get_correction`` for pending corrections.
  2. When a correction arrives, the agent applies it immediately.
  3. The agent reports the correction back via ``POST /hil/send_correction``
     so the decision agent can "learn" from it (record for later analysis).
  4. The agent periodically reports its state via ``POST /hil/send_status``.

All communication is JSON over HTTP and is fully optional: if the HIL
server is not running, the agent simply continues autonomously.

This module is domain-agnostic. The server side lives in
``src/hil_server.py``.

Safety note
-----------
HIL corrections are intended for local, controlled demo / research
environments. See ``docs/safety-boundaries.md``.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

import requests

logger = logging.getLogger("HilClient")

# Default HIL protocol version header.
HIL_VERSION = "1.0"


class HilClient:
    """HTTP client for the HIL correction server.

    Parameters
    ----------
    config:
        Application config dict. Recognised keys:
          * ``hil_server_url`` - base URL of the HIL server
          * ``script_id`` - unique identifier for this agent run
    """

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or {}
        self.server_url = self.config.get(
            "hil_server_url",
            os.getenv("HIL_SERVER_URL", "http://localhost:8001/hil"),
        )
        self.headers = {
            "Content-Type": "application/json",
            "HIL-Version": HIL_VERSION,
        }
        # A unique identifier for this agent run. Defaults to a generic name.
        self.script_id = self.config.get("script_id", "vision_fsm_agent")
        logger.info("HIL client ready, server=%s", self.server_url)

    # ------------------------------------------------------------------
    # Corrections
    # ------------------------------------------------------------------
    def get_manual_correction(self) -> dict[str, Any] | None:
        """Poll for a pending manual correction.

        Returns the correction dict, or ``None`` if nothing is pending or
        the server is unreachable.

        Example correction::

            {
                "type": "correct",
                "action": "click",
                "scene": "demo_grid",
                "correct_params": {"x": 150, "y": 220},
                "reason": "offset caused a miss"
            }
        """
        try:
            response = requests.get(
                f"{self.server_url}/get_correction",
                headers=self.headers,
                timeout=2,
            )
            if response.status_code == 200:
                correction = response.json()
                if self._validate_correction(correction):
                    logger.info("Received correction: %s", correction)
                    return correction
                logger.warning("Invalid correction format: %s", correction)
        except requests.exceptions.Timeout:
            logger.debug("HIL poll timed out (server may be down)")
        except Exception as exc:  # pragma: no cover - network edge cases
            logger.error("Failed to get correction: %s", exc)
        return None

    def send_status(self, status: dict[str, Any]) -> bool:
        """Report the current agent state to the HIL server."""
        try:
            payload = {
                "type": "agent_status",
                "script_id": self.script_id,
                "status": status,
                "timestamp": time.time(),
            }
            response = requests.post(
                f"{self.server_url}/send_status",
                headers=self.headers,
                json=payload,
                timeout=2,
            )
            if response.status_code == 200:
                return True
            logger.warning("Status report failed: HTTP %s", response.status_code)
        except Exception as exc:  # pragma: no cover - network edge cases
            logger.debug("Status report error: %s", exc)
        return False

    def send_correction_to_agent(self, correction: dict[str, Any]) -> bool:
        """Forward a manual correction to the decision agent for learning."""
        if not correction:
            return False
        try:
            payload = {
                "type": "manual_correction",
                "script_id": self.script_id,
                "correction": correction,
                "timestamp": time.time(),
            }
            response = requests.post(
                f"{self.server_url}/send_correction",
                headers=self.headers,
                json=payload,
                timeout=2,
            )
            if response.status_code == 200:
                logger.info("Correction forwarded to agent for learning")
                return True
            logger.warning("Forward correction failed: HTTP %s", response.status_code)
        except Exception as exc:  # pragma: no cover - network edge cases
            logger.error("Forward correction error: %s", exc)
        return False

    def get_agent_decision(self, agent_state: dict[str, Any]) -> dict[str, Any] | None:
        """Request a learned decision from the HIL/decision service."""
        try:
            payload = {
                "type": "request_decision",
                "script_id": self.script_id,
                "agent_state": agent_state,
                "timestamp": time.time(),
            }
            response = requests.post(
                f"{self.server_url}/get_decision",
                headers=self.headers,
                json=payload,
                timeout=3,
            )
            if response.status_code == 200:
                decision = response.json()
                logger.info("Received decision: %s", decision.get("action"))
                return decision
            logger.warning("Decision request failed: HTTP %s", response.status_code)
        except Exception as exc:  # pragma: no cover - network edge cases
            logger.debug("Decision request error: %s", exc)
        return None

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    @staticmethod
    def _validate_correction(correction: dict[str, Any]) -> bool:
        """Validate that a correction dict has the required fields."""
        if correction.get("type") == "none":
            return True
        required = ["type", "action", "correct_params"]
        for field in required:
            if field not in correction:
                logger.warning("Correction missing field: %s", field)
                return False
        if correction["action"] == "click":
            params = correction.get("correct_params", {})
            if "x" not in params or "y" not in params:
                logger.warning("Click correction missing x/y")
                return False
        return True
