---
title: "graph_node_drag_tool.py — GraphNodeDragTool"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_node_drag_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, drag]
---

# graph_node_drag_tool.py — GraphNodeDragTool

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
Enables right-click drag to reposition graph nodes. Extends Enable's ValueDragTool. On drag start, finds which node is under the cursor. During drag, updates the node's x/y position by the delta and requests redraw. Changes cursor to "hand" while dragging.

## Key Claims
- Triggered by right-click (drag_button = 'right') (confidence: high)
- Hit-tests all components to find the node under the cursor (confidence: high)
- Edges redraw live during drag because node position changes trigger container redraw (confidence: high)

## Relevance
One of three interaction tools. Shows the ValueDragTool pattern from Enable.

## Pages Updated
- [[GraphNodeDragTool]] — primary documentation source
- [[Interactive-Tools-Pattern]] — drag tool specifics
