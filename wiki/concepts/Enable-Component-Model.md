---
title: "Enable Component Model"
type: concept
confidence: 0.85
sources:
  - graphcanvas/graph_view.py
  - graphcanvas/graph_container.py
  - graphcanvas/graph_node_component.py
last_updated: 2026-05-19
stale: false
tags: [architecture, enable, enthought]
---

# Enable Component Model

## Definition
Graphcanvas is built on Enthought's Enable toolkit, which provides a component/container hierarchy for 2D interactive graphics. Components are leaf-level drawable objects, Containers hold and manage collections of Components, and Tools attach interactive behavior to Components or Containers.

## Evidence

### From graph_container.py
GraphContainer extends `enable.api.Container`. It manages child components (nodes), handles layout, and custom-draws edges using the Kiva graphics context (`gc`). The `draw()` method receives a graphics context and view bounds — the standard Enable rendering interface.

### From graph_node_component.py
GraphNodeComponent extends `enable.api.Component`. It implements `draw()` with the same signature. It has `x`, `y`, `width`, `height` attributes inherited from Component for positioning.

### From graph_view.py
The view layer uses Enable's `Viewport` (for zoom), `Scrolled` (for scroll), `ComponentEditor` (for TraitsUI embedding), and `ViewportPanTool` (for pan). This shows the full Enable stack: Component → Container → Viewport → Scrolled → TraitsUI.

## Key Patterns
1. **Container/Component hierarchy** — Container.components holds children, calls their draw()
2. **Tools** — Behavior objects attached to components via `component.tools.append(tool)`
3. **Kiva graphics context** — All rendering via `gc` methods (move_to, curve_to, arc_to, etc.)
4. **Trait-driven updates** — `request_redraw()` triggers the Enable rendering pipeline

## Related Concepts
- [[Interactive-Tools-Pattern]]
- [[Graph-Layout-Algorithms]]
