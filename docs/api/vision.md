# Vision API Reference

## `TemplateManager`

Manages a collection of named templates and matches them against frames.

### Constructor

```python
TemplateManager(
    confidence_threshold: float = 0.8,
    scale_range: tuple[float, float] = (0.6, 1.4),
    scale_steps: int = 10,
)
```

### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `add_from_array(name, template)` | `None` | Add a template from an in-memory array |
| `add_from_file(name, path)` | `bool` | Load a template from disk |
| `load_directory(directory, prefix="", suffix=".png")` | `int` | Load all images in a directory |
| `match_one(name, frame)` | `MatchResult` | Match a single named template |
| `match_best(frame)` | `MatchResult` | Match all, return highest confidence |
| `match_all(frame)` | `list[MatchResult]` | Match all, sorted by confidence desc |

### Properties

| Property | Type | Description |
|----------|------|-------------|
| `names` | `list[str]` | All template names |
| `confidence_threshold` | `float` | Minimum confidence for `found=True` |
| `scale_range` | `tuple` | Multi-scale range |
| `scale_steps` | `int` | Number of scale steps |

## `MatchResult`

Result of matching a template against a frame (dataclass).

| Field | Type | Description |
|-------|------|-------------|
| `found` | `bool` | Whether confidence ≥ threshold |
| `confidence` | `float` | Best match confidence (0.0–1.0) |
| `position` | `tuple[int, int]` | Top-left of best match |
| `center` | `tuple[int, int]` | Center of matched region |
| `template_name` | `str` | Name of matched template |
| `template_shape` | `tuple[int, int] \| None` | (h, w) of matched template |

## `multi_scale_match`

Low-level multi-scale template matching.

```python
multi_scale_match(
    template: np.ndarray,
    screenshot: np.ndarray,
    scale_range: tuple[float, float] = (0.6, 1.4),
    scale_steps: int = 10,
) -> tuple[float, tuple[int, int]]
```

Returns `(best_confidence, best_position)`.

## Example

```python
from vision import TemplateManager
import cv2

mgr = TemplateManager(confidence_threshold=0.75)
mgr.load_directory("assets/demo")

frame = cv2.imread("some_frame.png")
result = mgr.match_best(frame)

if result.found:
    print(f"Found {result.template_name} at {result.center} "
          f"(confidence={result.confidence:.3f})")
```
