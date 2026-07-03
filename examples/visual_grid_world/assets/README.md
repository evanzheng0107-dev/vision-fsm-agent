# Demo Assets

All images in this directory are **programmatically generated** by
`scripts/generate_demo_assets.py`. They contain no third-party content.

| File | Description |
|------|-------------|
| `target_goal.png` | Green crosshair — navigation target |
| `pickup_item.png` | Gold circle — collectible item |
| `interact_button.png` | Blue square — interactable button |

## Regenerating

```bash
python scripts/generate_demo_assets.py
```

The drawing primitives live in
`src/vision_fsm_agent/envs/grid_world.py` and are shared with the
`DemoEnvironment` renderer, guaranteeing that template matching finds
the elements in rendered frames.
