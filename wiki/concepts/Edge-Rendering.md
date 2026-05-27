---
title: "Edge Rendering"
type: concept
confidence: 0.85
sources:
  - graphcanvas/graph_container.py
last_updated: 2026-05-19
stale: false
tags: [rendering, edges, bezier]
---

# Edge Rendering

## Definition
Edges between graph nodes are rendered as cubic Bézier curves with smart endpoint selection based on the relative positions of source and destination nodes. Directed graphs additionally receive arrowheads at both endpoints.

## Endpoint Selection Logic
The algorithm selects which side of each node the edge connects to:

| Condition | Origin side | Destination side |
|-----------|------------|-----------------|
| dy > abs(dx) | Bottom | Top |
| dy < -abs(dx) | Top | Bottom |
| dx > abs(dy) | Left | Right |
| dx < -abs(dy) | Right | Left |
| else (self-loop) | Right | Bottom |

Control points are offset by 1/3 of the distance to create smooth curves.

## Arrowheads (Directed Graphs)
- **Origin dots** — Small arcs (radius 3) at line start, oriented by direction
- **Destination arrows** — V-shaped arrowheads using rotation matrices (30-degree angle, 10px length)

## Weighted Edges
Edges with `weight < 0.5` render as dashed lines (pattern [5,5], CAP_BUTT).

## Open Questions
- Edge color hardcoded to gray (0.5, 0.5, 0.5)
- No edge labels
- No curved edge avoidance (edges can overlap nodes)
- Arrowhead logic uses numpy matrix operations — efficient for batch but complex to read

## Related Concepts
- [[Graph-Layout-Algorithms]]
- [[Enable-Component-Model]]
