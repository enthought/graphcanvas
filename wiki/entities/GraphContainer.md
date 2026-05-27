---
title: "GraphContainer"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_container.py
  - graphcanvas/graph_view.py
last_updated: 2026-05-19
stale: false
tags: [container, layout, rendering, public-api]
---

# GraphContainer

## Overview
The core Enable Container subclass responsible for graph layout computation and edge rendering. Holds GraphNodeComponent instances as children and draws Bézier-curve edges between them.

## Key Attributes
- `graph` — Instance(networkx.Graph). The NetworkX graph data.
- `style` — Enum of SUPPORTED_LAYOUTS ('spring', 'tree', 'shell', 'circular', 'spectral').
- `_graph_layout_needed` — Bool flag to cache expensive layout computation.
- `bounds` — Auto-resized to fit the current graph.

## Responsibilities
1. **Layout** — Computes node positions via NetworkX layout algorithms. See [[Graph-Layout-Algorithms]].
2. **Edge Drawing** — Renders edges as cubic Bézier curves with smart endpoint selection. See [[Edge-Rendering]].
3. **Arrowheads** — Draws directional arrowheads for directed graphs using rotation matrices.
4. **Weighted Edges** — Renders dashed lines for edges with weight < 0.5.

## Relationships
- Parent of [[GraphNodeComponent]] instances
- Subclassed by [[DAGContainer]]
- Created by [[GraphView]]
- Part of [[Enable-Component-Model]]

## Open Questions
- The `draw` method is ~150 lines — potential candidate for decomposition
- Edge styling (color, width) is hardcoded, not configurable via traits
