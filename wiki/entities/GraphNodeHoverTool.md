---
title: "GraphNodeHoverTool"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_node_hover_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, hover]
---

# GraphNodeHoverTool

## Overview
Detects mouse hover over graph nodes and invokes a callback with the node's label. Extends Enable's HoverTool (which handles hover timing/threshold logic).

## Key Attributes
- `_last_xy` — Tuple tracking current mouse position
- `callback` — Callable invoked with the hovered node's label string

## Behavior
1. `normal_mouse_move()` — tracks mouse position, delegates to HoverTool
2. `on_hover()` — hit-tests components at `_last_xy`, calls callback with label

## Relationships
- Attached to [[GraphContainer]] by [[GraphView]]
- Part of [[Interactive-Tools-Pattern]]
- Targets [[GraphNodeComponent]] instances
