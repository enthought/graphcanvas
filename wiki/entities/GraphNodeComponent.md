---
title: "GraphNodeComponent"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_node_component.py
last_updated: 2026-05-19
stale: false
tags: [component, node, rendering, public-api]
---

# GraphNodeComponent

## Overview
An Enable Component representing a single graph node. Renders as a rounded rectangle with gradient fill and centered text label. Self-sizes based on label text extent.

## Key Attributes
- `value` — Any. The underlying data object this node represents.
- `label` — Property(Unicode). Derived from value.label or str(value), max 20 chars.
- `level` — Int. Depth from root (used in tree layout).
- `_key` — Any. The graph dictionary key used for layout position lookups.
- Padding: 5px on all sides.

## Rendering
1. Sets font to MODERN family
2. Measures text extent → sets component width/height
3. Draws rounded-rect border with gradient (cyan → red)
4. Draws label text at padding offset

## Relationships
- Child of [[GraphContainer]]
- Targeted by [[GraphNodeDragTool]], [[GraphNodeHoverTool]], [[GraphNodeSelectionTool]]
- Part of [[Enable-Component-Model]]

## Open Questions
- Gradient colors are hardcoded — no theming support
- Font family hardcoded to MODERN
- No selection highlight state
