---
title: "Graph Layout Algorithms"
type: concept
confidence: 0.85
sources:
  - graphcanvas/graph_container.py
  - graphcanvas/layout.py
last_updated: 2026-05-19
stale: false
tags: [algorithm, layout, networkx]
---

# Graph Layout Algorithms

## Definition
Graphcanvas supports five graph layout algorithms that compute 2D positions for nodes. Four delegate to NetworkX (with optional pygraphviz acceleration). One (`tree_layout`) is a custom implementation providing a fallback when pygraphviz is unavailable.

## Supported Layouts

| Style | Implementation | Fallback | Notes |
|-------|---------------|----------|-------|
| spring | `networkx.spring_layout` | — | Force-directed. Uses initial positions if non-zero. |
| tree | `pygraphviz_layout(prog='dot')` | Custom `tree_layout` | Requires DAG for fallback. |
| shell | `networkx.shell_layout` | — | Concentric circles. |
| circular | `pygraphviz_layout(prog='twopi')` | `networkx.circular_layout` | — |
| spectral | `networkx.spectral_layout` | — | Eigenvector-based. |

## Custom tree_layout (layout.py)
- Only supports 2D directed acyclic graphs
- Identifies roots as nodes with in-degree 0
- Traverses via stack (depth-first despite BFS comment)
- Positions: vertical = depth level, horizontal = center-aligned via linspace

## Layout Caching
The `_graph_layout_needed` flag prevents recomputation. Set to True on graph change, reset to False after `do_layout()` completes.

## Bounds Resizing
Each layout style computes appropriate container bounds based on node count and size. This ensures the viewport can scroll to all nodes.

## Open Questions
- No animated transitions between layouts
- Spring layout doesn't iterate to convergence — single pass
- Custom tree_layout uses stack (DFS) but comments say "breadth first"

## Related Concepts
- [[Enable-Component-Model]]
- [[Edge-Rendering]]
