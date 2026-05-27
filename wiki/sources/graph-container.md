---
title: "graph_container.py — GraphContainer"
type: source
confidence: 0.95
sources:
  - graphcanvas/graph_container.py
last_updated: 2026-05-19
stale: false
tags: [container, layout, rendering, edges]
---

# graph_container.py — GraphContainer

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
The core rendering container. Extends Enable's Container to manage graph layout and edge drawing. Supports five layout algorithms (spring, tree, shell, circular, spectral) via NetworkX. Handles edge rendering with cubic Bézier curves, directional arrowheads, and weighted edge styling (dashed lines for weight < 0.5).

## Key Claims
- Five layout styles supported: spring, tree, shell, circular, spectral (confidence: high)
- Tree layout falls back from pygraphviz to custom `tree_layout` if pygraphviz unavailable (confidence: high)
- Edge drawing uses cubic Bézier curves with smart origin/destination point selection based on relative node positions (confidence: high)
- Directed graphs get arrowheads drawn using rotation matrices (confidence: high)
- Layout is expensive and cached via `_graph_layout_needed` flag (confidence: high)
- Container auto-resizes bounds to fit the graph for each layout style (confidence: high)

## Relevance
The most complex file in the codebase. Contains both the layout engine and the rendering engine for edges. Understanding this file is critical for anyone modifying visual behavior.

## Pages Updated
- [[GraphContainer]] — primary documentation source
- [[Graph-Layout-Algorithms]] — all five layout algorithms documented here
- [[Enable-Component-Model]] — Container subclass pattern
- [[Edge-Rendering]] — Bézier curve and arrowhead logic
