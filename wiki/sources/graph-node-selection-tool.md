---
title: "graph_node_selection_tool.py — GraphNodeSelectionTool"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_node_selection_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, selection]
---

# graph_node_selection_tool.py — GraphNodeSelectionTool

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
Handles double-click on graph nodes to open a traits editor. Extends Enable's BaseTool. If the node's value is a HasTraits instance, calls `edit_traits()` on the value. Otherwise, opens a livemodal editor on the node component itself.

## Key Claims
- Triggered by left double-click (confidence: high)
- Two behavior paths: HasTraits values get their own editor, other values use the component's editor (confidence: high)
- Simplest of the three tools — 20 lines total (confidence: high)

## Relevance
One of three interaction tools. Provides the inspection/editing affordance for graph nodes.

## Pages Updated
- [[GraphNodeSelectionTool]] — primary documentation source
- [[Interactive-Tools-Pattern]] — selection tool specifics
