"""
Computer-vision engine based on multi-scale template matching.

This module wraps OpenCV's ``cv2.matchTemplate`` with:

  * Configurable scale ranges for robustness to size variation
  * Multi-template management (match against many templates, keep the best)
  * Structured :class:`MatchResult` outputs suitable for FSM events

The engine is domain-agnostic: it operates on any ``numpy`` image array
and any grayscale template array. The demo application
(``demo_app/visual_grid_world.py``) generates synthetic frames and
templates so the full agent loop runs without any external imagery.

Safety note
-----------
Vision results feed into an FSM that may trigger automated actions.
Such automation must stay within the safety boundaries documented in
``docs/safety-boundaries.md`` (local, controlled demo / research / education
only).
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    """Result of matching a single (or set of) template(s) against a frame."""

    found: bool
    confidence: float
    position: Tuple[int, int]  # top-left of best match in the frame
    center: Tuple[int, int]  # center of the matched template region
    template_name: str = ""
    template_shape: Optional[Tuple[int, int]] = None  # (h, w) of matched template

    def __repr__(self) -> str:  # pragma: no cover - trivial
        status = "FOUND" if self.found else "miss"
        return (
            f"MatchResult({status} conf={self.confidence:.3f} "
            f"center={self.center} tpl={self.template_name!r})"
        )


# ----------------------------------------------------------------------
# Low-level matching
# ----------------------------------------------------------------------
def multi_scale_match(
    template: np.ndarray,
    screenshot: np.ndarray,
    scale_range: Tuple[float, float] = (0.6, 1.4),
    scale_steps: int = 10,
) -> Tuple[float, Tuple[int, int]]:
    """Match ``template`` against ``screenshot`` across multiple scales.

    Parameters
    ----------
    template:
        Grayscale template image (HxW, uint8).
    screenshot:
        Grayscale or BGR frame. Converted to grayscale internally.
    scale_range:
        ``(min_scale, max_scale)`` inclusive.
    scale_steps:
        Number of evenly spaced scales to try. Must be >= 2.

    Returns
    -------
    (best_confidence, best_position)
        ``best_position`` is the top-left corner of the best match in
        the *grayscale* frame coordinates.
    """
    if template is None or screenshot is None:
        return 0.0, (0, 0)

    # Ensure both are grayscale so cv2.matchTemplate types match.
    if template.ndim == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    scale_start, scale_end = scale_range
    if scale_steps < 2:
        scale_steps = 2
    scale_step = (scale_end - scale_start) / (scale_steps - 1)
    scales = [scale_start + i * scale_step for i in range(scale_steps)]

    best_val = 0.0
    best_pos = (0, 0)

    # Ensure grayscale
    if screenshot.ndim == 3:
        gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    else:
        gray_screenshot = screenshot

    for scale in scales:
        resized = cv2.resize(template, (0, 0), fx=scale, fy=scale)
        th, tw = resized.shape[:2]
        sh, sw = gray_screenshot.shape[:2]
        if th > sh or tw > sw:
            continue
        result = cv2.matchTemplate(gray_screenshot, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > best_val:
            best_val = max_val
            best_pos = (int(max_loc[0]), int(max_loc[1]))

    return float(best_val), best_pos


# ----------------------------------------------------------------------
# Template manager
# ----------------------------------------------------------------------
class TemplateManager:
    """Load and match a collection of named templates.

    Templates are stored as grayscale ``np.ndarray`` keyed by name.

    Example
    -------
    >>> mgr = TemplateManager(confidence_threshold=0.8)
    >>> mgr.add_from_array("button", button_gray)
    >>> result = mgr.match_best(frame)  # best match across all templates
    """

    def __init__(
        self,
        confidence_threshold: float = 0.8,
        scale_range: Tuple[float, float] = (0.6, 1.4),
        scale_steps: int = 10,
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.scale_range = scale_range
        self.scale_steps = scale_steps
        self._templates: Dict[str, np.ndarray] = {}

    # -- loading --
    def add_from_array(self, name: str, template: np.ndarray) -> None:
        """Add a template from an in-memory array (auto-converted to grayscale)."""
        if template is None:
            logger.warning("Skipping None template %r", name)
            return
        gray = template if template.ndim == 2 else cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        self._templates[name] = gray
        logger.debug("Loaded template %r shape=%s", name, gray.shape)

    def add_from_file(self, name: str, path: str) -> bool:
        """Load a template image from disk. Returns True on success."""
        if not os.path.exists(path):
            logger.warning("Template not found: %s", path)
            return False
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            logger.warning("Failed to read template: %s", path)
            return False
        self._templates[name] = img
        logger.debug("Loaded template %r from %s shape=%s", name, path, img.shape)
        return True

    def load_directory(
        self, directory: str, prefix: str = "", suffix: str = ".png"
    ) -> int:
        """Load all image files in ``directory`` matching ``prefix``/``suffix``.

        Returns the number of templates loaded.
        """
        if not os.path.isdir(directory):
            logger.warning("Directory not found: %s", directory)
            return 0
        count = 0
        for fname in sorted(os.listdir(directory)):
            if not fname.lower().endswith(suffix):
                continue
            if prefix and not fname.startswith(prefix):
                continue
            name = os.path.splitext(fname)[0]
            if self.add_from_file(name, os.path.join(directory, fname)):
                count += 1
        logger.info("Loaded %d templates from %s", count, directory)
        return count

    # -- inspection --
    @property
    def names(self) -> List[str]:
        return list(self._templates.keys())

    def __len__(self) -> int:
        return len(self._templates)

    def __contains__(self, name: str) -> bool:
        return name in self._templates

    # -- matching --
    def match_one(self, name: str, frame: np.ndarray) -> MatchResult:
        """Match a single named template against ``frame``."""
        template = self._templates.get(name)
        if template is None:
            return MatchResult(False, 0.0, (0, 0), (0, 0), template_name=name)
        val, pos = multi_scale_match(
            template, frame, self.scale_range, self.scale_steps
        )
        th, tw = template.shape[:2]
        center = (pos[0] + tw // 2, pos[1] + th // 2)
        return MatchResult(
            found=val >= self.confidence_threshold,
            confidence=val,
            position=pos,
            center=center,
            template_name=name,
            template_shape=(th, tw),
        )

    def match_best(self, frame: np.ndarray) -> MatchResult:
        """Match all templates, return the one with the highest confidence.

        If no templates are registered, returns a not-found result.
        """
        best = MatchResult(False, 0.0, (0, 0), (0, 0))
        for name in self._templates:
            res = self.match_one(name, frame)
            if res.confidence > best.confidence:
                best = res
        return best

    def match_all(self, frame: np.ndarray) -> List[MatchResult]:
        """Match every template, returning a list sorted by confidence desc."""
        results = [self.match_one(name, frame) for name in self._templates]
        results.sort(key=lambda r: r.confidence, reverse=True)
        return results
