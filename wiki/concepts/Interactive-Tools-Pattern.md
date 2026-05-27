---
title: "Interactive Tools Pattern"
type: concept
confidence: 0.85
sources:
  - graphcanvas/graph_node_drag_tool.py
  - graphcanvas/graph_node_hover_tool.py
  - graphcanvas/graph_node_selection_tool.py
  - graphcanvas/graph_view.py
last_updated: 2026-05-19
stale: false
tags: [architecture, interaction, tools]
---

# Interactive Tools Pattern

## Definition
Graphcanvas implements user interaction through Enable's Tool system. Tools are separate objects attached to a container that intercept input events (mouse clicks, moves, drags) and act on the container's child components. This separates interaction logic from rendering logic.

## Evidence

### Three tools, three interaction modes
| Tool | Trigger | Base Class | Behavior |
|------|---------|------------|----------|
| [[GraphNodeSelectionTool]] | Left double-click | BaseTool | Opens traits editor |
| [[GraphNodeHoverTool]] | Mouse hover (timed) | HoverTool | Calls callback with label |
| [[GraphNodeDragTool]] | Right-click drag | ValueDragTool | Repositions node |

### Attachment pattern (from graph_view.py)
All three tools are appended to the container's `tools` list in `__canvas_default()`. This is the standard Enable pattern — tools are composable and order-independent.

### Hit-testing pattern
All three tools share the same hit-test approach: iterate `self.component.components` and call `node.is_in(x, y)`. This is a linear scan — no spatial indexing.

## Contradictions
None across sources.

## Open Questions
- No mechanism for users to add custom tools without subclassing GraphView
- Hit-testing is O(n) — could be slow for large graphs
- No keyboard interaction tools

## Related Concepts
- [[Enable-Component-Model]]
- [[Container-Component-Architecture]]
