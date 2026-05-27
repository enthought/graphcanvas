---
title: "GraphView"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_view.py
  - graphcanvas/api.py
last_updated: 2026-05-19
stale: false
tags: [view, orchestrator, public-api]
---

# GraphView

## Overview
The top-level widget class that ties together all graphcanvas components into a usable, interactive graph visualization. A HasTraits class providing a TraitsUI View with a scrollable, zoomable canvas.

## Key Attributes
- `graph` — Instance(networkx.Graph). The data to visualize.
- `nodes` — Property(List). Derived from graph.nodes().
- `layout` — Enum of SUPPORTED_LAYOUTS. Controls graph layout algorithm.
- `_canvas` — The GraphContainer or DAGContainer instance.
- `_container` — Scrolled wrapper providing viewport with zoom/pan.

## Architecture
1. Accepts a NetworkX graph
2. Auto-selects container type (DAGContainer if directed, GraphContainer otherwise)
3. Attaches three interaction tools: [[GraphNodeSelectionTool]], [[GraphNodeHoverTool]], [[GraphNodeDragTool]]
4. Wraps canvas in Viewport (zoom) + Scrolled (scrollbars)
5. Adds ViewportPanTool for viewport-level panning

## Relationships
- Contains [[GraphContainer]] or [[DAGContainer]] as canvas
- Uses [[GraphNodeComponent]] instances for each node
- Part of [[Enable-Component-Model]] architecture
- Implements [[Interactive-Tools-Pattern]]

## Open Questions
- No mechanism for custom tool injection beyond subclassing
- Hover callback is hardcoded to print — no event system for external listeners
