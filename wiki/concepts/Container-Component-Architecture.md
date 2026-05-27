---
title: "Container-Component Architecture"
type: concept
confidence: 0.85
sources:
  - graphcanvas/graph_view.py
  - graphcanvas/graph_container.py
  - graphcanvas/dag_container.py
  - graphcanvas/graph_node_component.py
last_updated: 2026-05-19
stale: false
tags: [architecture, patterns, design]
---

# Container-Component Architecture

## Definition
Graphcanvas uses a layered containment hierarchy where each level has a specific responsibility. This is the structural pattern that organizes all visual elements.

## The Stack (outside → inside)

```
Scrolled (scroll bars)
  └── Viewport (zoom, pan)
        └── GraphContainer / DAGContainer (layout, edge drawing)
              └── GraphNodeComponent × N (node rendering)
```

## Responsibilities by Layer

| Layer | Class | Responsibility |
|-------|-------|---------------|
| Outermost | Scrolled | Scroll bars, clipping |
| Viewport | Viewport + ViewportPanTool | Zoom, pan, view position |
| Canvas | GraphContainer | Node layout, edge drawing, tool host |
| Leaf | GraphNodeComponent | Individual node rendering |

## Data Flow
1. User sets `GraphView.graph` (a NetworkX graph)
2. `_graph_changed` clears old components, creates new GraphNodeComponent per node
3. Container marks `_graph_layout_needed = True`
4. On next `draw()`, `do_layout()` computes positions
5. Each component draws itself, then container draws edges

## Related Concepts
- [[Enable-Component-Model]]
- [[Interactive-Tools-Pattern]]
- [[Graph-Layout-Algorithms]]
