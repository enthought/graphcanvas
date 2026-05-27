---
title: "GraphNodeDragTool"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_node_drag_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, drag]
---

# GraphNodeDragTool

## Overview
Enables right-click drag repositioning of graph nodes. Extends Enable's ValueDragTool. Edges redraw live during drag because node position changes trigger container redraw.

## Key Attributes
- `drag_button` — 'right'
- `x_name` / `y_name` — 'x' / 'y' (position attributes to modify)

## Behavior
1. `get_value()` — hit-tests all components at click point, returns the node under cursor
2. `set_delta()` — updates node.x/y to original + delta, requests redraw
3. `dragging()` — sets cursor to "hand"

## Relationships
- Attached to [[GraphContainer]] by [[GraphView]]
- Part of [[Interactive-Tools-Pattern]]
- Targets [[GraphNodeComponent]] instances
