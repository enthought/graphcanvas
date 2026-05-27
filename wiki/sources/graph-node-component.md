---
title: "graph_node_component.py — GraphNodeComponent"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_node_component.py
last_updated: 2026-05-19
stale: false
tags: [component, node, rendering]
---

# graph_node_component.py — GraphNodeComponent

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
The visual representation of a single graph node. Extends Enable's Component. Renders a rounded-rectangle border with a gradient fill and a text label. Auto-sizes based on text extent. Supports any value type — uses `value.label` if available, otherwise `str(value)`, truncated to 20 characters.

## Key Claims
- Node size is dynamic, computed from text extent plus padding (confidence: high)
- Border drawn with rounded corners (radius=4) using arc_to (confidence: high)
- Gradient fill from cyan to red (starting_color → ending_color) (confidence: high)
- Label truncated to 20 chars with "..." suffix (confidence: high)
- The `_key` attribute is the graph dictionary key for layout lookups (confidence: high)

## Relevance
The leaf-level visual element. Every node in the graph becomes one of these. Key extension point for custom node rendering.

## Pages Updated
- [[GraphNodeComponent]] — primary documentation source
- [[Enable-Component-Model]] — Component subclass pattern
