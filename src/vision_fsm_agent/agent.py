"""
Decision agents for the Vision FSM Agent framework.

Two implementations are provided:

* :class:`LocalDecisionAgent` - pure-Python rule-based decisions. Works
  offline with zero configuration. This is what the demo uses by default.
* :class:`CloudDecisionAgent` - optional LLM-backed decisions via an
  OpenAI-compatible API (configured through environment variables). Falls
  back gracefully on errors.

Both agents share the same interface::

    agent = LocalDecisionAgent()
    decision = agent.get_decision(agent_state)
    # decision == {"action": "move", "reason": "target detected"}

The ``agent_state`` dict is produced by the main loop and typically
contains vision match results, the current FSM state, and retry counters.

Safety note
-----------
Decisions drive automated actions. All automation must stay within the
safety boundaries documented in ``docs/safety-boundaries.md``.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

logger = logging.getLogger(__name__)

# Canonical action vocabulary. The FSM and main loop recognise these.
ACTIONS = ("move", "pickup", "interact", "explore", "wait", "continue")


class DecisionAgent:
    """Base interface for decision agents."""

    def get_decision(self, agent_state: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


# ----------------------------------------------------------------------
# Local rule-based agent
# ----------------------------------------------------------------------
class LocalDecisionAgent(DecisionAgent):
    """A deterministic, rule-based decision agent.

    Requires no network or API keys. Decisions are derived purely from
    the vision match results and retry counters in ``agent_state``.

    Decision priority:
      1. ``interact``  - an actionable button/element was detected
      2. ``pickup``    - a collectible item was detected
      3. ``move``      - a navigation target was detected
      4. ``wait``      - too many consecutive failures
      5. ``explore``   - nothing detected, perform blind exploration
    """

    def __init__(self, failure_threshold: int = 3) -> None:
        self.failure_threshold = failure_threshold
        self.decision_count = 0

    def get_decision(self, agent_state: dict[str, Any]) -> dict[str, Any]:
        self.decision_count += 1
        matches = agent_state.get("match_results", {})

        interact = matches.get("interact", {})
        pickup = matches.get("pickup", {})
        target = matches.get("target", {})

        if interact.get("found"):
            return {"action": "interact", "reason": "actionable element detected"}
        if pickup.get("found"):
            return {"action": "pickup", "reason": "collectible detected"}
        if target.get("found"):
            return {"action": "move", "reason": "navigation target detected"}

        failed = agent_state.get("failed_attempts", 0)
        if failed > self.failure_threshold:
            return {"action": "wait", "reason": f"{failed} consecutive failures, pausing"}

        return {
            "action": "explore",
            "reason": f"no targets detected (decision #{self.decision_count})",
        }


# ----------------------------------------------------------------------
# Optional cloud / LLM agent
# ----------------------------------------------------------------------
class CloudDecisionAgent(DecisionAgent):
    """An optional LLM-backed decision agent.

    Configured via environment variables (see ``.env.example``):

      * ``LLM_API_KEY``      - API key for the model provider
      * ``LLM_BASE_URL``     - OpenAI-compatible endpoint
      * ``LLM_MODEL``        - model name

    If the API key is missing or a request fails, it falls back to a
    :class:`LocalDecisionAgent` so the agent loop never blocks.
    """

    def __init__(self, fallback: DecisionAgent | None = None) -> None:
        # Import here so the module loads even if requests is unavailable.
        import requests  # noqa: F401  (ensure available)

        self.api_key = os.getenv("LLM_API_KEY")
        self.api_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.fallback = fallback or LocalDecisionAgent()
        self._json_pattern = re.compile(r"\{.*\}", re.DOTALL)
        if self.api_key:
            logger.info("CloudDecisionAgent configured (model=%s)", self.model)
        else:
            logger.info("CloudDecisionAgent has no API key; will use local fallback")

    def _extract_json(self, text: str) -> dict | None:
        """Best-effort extraction of a JSON object from model output."""
        try:
            return json.loads(text)
        except Exception:
            pass
        text = re.sub(r"```json\s*|\s*```", "", text)
        match = self._json_pattern.search(text)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        return None

    def get_decision(self, agent_state: dict[str, Any]) -> dict[str, Any]:
        if not self.api_key:
            return self.fallback.get_decision(agent_state)
        try:
            import requests

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a decision engine for a vision-driven "
                            "automation agent. Return ONLY a JSON object: "
                            '{"action": "move|pickup|interact|explore|wait|continue", '
                            '"reason": "short reason"}. No markdown, no prose.'
                        ),
                    },
                    {
                        "role": "user",
                        "content": json.dumps(agent_state, ensure_ascii=False),
                    },
                ],
                "max_tokens": 100,
                "temperature": 0.1,
            }
            response = requests.post(
                f"{self.api_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
            decision = self._extract_json(content)
            if decision and "action" in decision:
                if decision["action"] not in ACTIONS:
                    decision["action"] = "continue"
                return decision
            logger.warning("Could not parse cloud response: %s", content[:200])
        except Exception as exc:
            logger.warning("Cloud decision failed, using fallback: %s", exc)
        return self.fallback.get_decision(agent_state)
