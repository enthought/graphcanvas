---
title: "Graphcanvas Wiki Overview"
type: synthesis
confidence: 0.85
sources:
  - graphcanvas/api.py
  - graphcanvas/graph_view.py
  - graphcanvas/graph_container.py
  - graphcanvas/graph_node_component.py
  - graphcanvas/layout.py
  - graphcanvas/dag_container.py
  - graphcanvas/graph_node_drag_tool.py
  - graphcanvas/graph_node_hover_tool.py
  - graphcanvas/graph_node_selection_tool.py
last_updated: 2026-05-19
stale: false
tags: [overview, architecture]
---

# Graphcanvas — Overview

## What It Is
Graphcanvas is an interactive graph (network) visualization library built on Enthought's Enable toolkit and NetworkX. It renders directed and undirected graphs with draggable nodes, hover tooltips, and double-click editing.

## Architecture Summary
The library follows a strict layered containment hierarchy:

```
GraphView (HasTraits orchestrator)
  → Scrolled → Viewport (zoom/pan)
    → GraphContainer (layout + edge rendering)
      → GraphNodeComponent × N (node visuals)
        + Tools (drag, hover, selection)
```

## Key Design Decisions
1. **Enable over matplotlib** — Provides real-time interactivity (drag, zoom, hover) that static plotting libraries cannot.
2. **Tools as separate objects** — Interaction behaviors are composable, not baked into components.
3. **NetworkX for layout** — Delegates graph algorithms to NetworkX; only `tree_layout` is custom.
4. **Container owns edge drawing** — Edges are not components; they're drawn by the container after all node components render.
5. **Trait-driven updates** — Changes to graph data propagate automatically via Traits observers.

## Major Themes
- **Simplicity** — ~570 lines of non-test code total. Minimal but functional.
- **Extensibility via Enable** — Leverages Enable's full stack (Component, Container, Tool, Viewport).
- **Graceful degradation** — Falls back from pygraphviz to pure-Python layouts.

## Known Gaps / Open Questions
- No theming/styling API (colors, fonts hardcoded)
- No edge labels
- No selection state or multi-select
- O(n) hit-testing — no spatial index
- Hover callback hardcoded to print in GraphView
- No keyboard shortcuts
- Python 2/3 transition artifacts (six, `from __future__`)

## Unresolved Contradictions
- dag_container.py's docstring says "Enable Container for Directed Acyclic Graphs" but no acyclicity is enforced at the container level (only in tree_layout)
- layout.py comment says "breadth first tree traversal" but implementation uses a stack (DFS)
