---
title: "graph_view.py — GraphView and graph_from_dict"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_view.py
last_updated: 2026-05-19
stale: false
tags: [view, traits, orchestration]
---

# graph_view.py — GraphView and graph_from_dict

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
Contains the top-level `GraphView` class (a HasTraits model+view) and the `graph_from_dict` utility function. GraphView orchestrates all other components: it holds a NetworkX graph, creates the canvas (GraphContainer or DAGContainer), attaches all three interaction tools, and wraps everything in a scrollable, zoomable viewport.

## Key Claims
- GraphView auto-selects DAGContainer for directed graphs, GraphContainer otherwise (confidence: high)
- Three tools are always attached: selection, hover, drag (confidence: high)
- graph_from_dict creates a DiGraph from an adjacency-list dictionary (confidence: high)
- The view supports zoom via Enable's Viewport and pan via ViewportPanTool (confidence: high)
- Node trait changes trigger canvas redraw when nodes are HasTraits instances (confidence: high)

## Relevance
This is the orchestrator — the single class that ties together the container, components, and tools into a usable widget. Understanding GraphView is essential for understanding how the library works end-to-end.

## Pages Updated
- [[GraphView]] — primary documentation source
- [[GraphContainer]] — instantiation and configuration context
- [[DAGContainer]] — conditional instantiation logic
- [[Interactive-Tools-Pattern]] — tool attachment pattern
- [[Enable-Component-Model]] — viewport/scrolled architecture
