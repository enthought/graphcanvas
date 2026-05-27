---
title: "graph_node_hover_tool.py — GraphNodeHoverTool"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_node_hover_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, hover]
---

# graph_node_hover_tool.py — GraphNodeHoverTool

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
Detects mouse hover over graph nodes and invokes a callback with the hovered node's label. Extends Enable's HoverTool. Tracks mouse position via `_last_xy` and on hover triggers a hit-test against all child components.

## Key Claims
- Uses Enable's HoverTool with its built-in hover timing logic (confidence: high)
- Callback receives the node's label string (confidence: high)
- Hit-tests child components to identify which node is being hovered (confidence: high)

## Relevance
One of three interaction tools. Enables tooltip-like behavior and custom hover callbacks.

## Pages Updated
- [[GraphNodeHoverTool]] — primary documentation source
- [[Interactive-Tools-Pattern]] — hover tool specifics
