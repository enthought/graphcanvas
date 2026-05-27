---
title: "layout.py — Custom Tree Layout Algorithm"
type: source
confidence: 0.95
sources:
  - graphcanvas/layout.py
last_updated: 2026-05-19
stale: false
tags: [layout, tree, algorithm]
---

# layout.py — Custom Tree Layout Algorithm

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
Provides a custom `tree_layout` function as a fallback when pygraphviz is not installed. Computes 2D positions for DAG nodes using breadth-first traversal from root nodes (nodes with in-degree 0). Positions are justified horizontally at each depth level using linspace.

## Key Claims
- Only supports 2D layout (confidence: high)
- Requires a directed acyclic graph — raises ValueError otherwise (confidence: high)
- Roots identified as nodes with in-degree == 0 (confidence: high)
- Uses breadth-first traversal with a stack (actually DFS despite comment saying BFS) (confidence: medium)
- Horizontal positions center-aligned at each depth via numpy.linspace (confidence: high)

## Relevance
The only custom algorithm in the codebase. All other layouts delegate to NetworkX. This is the fallback for tree layout when pygraphviz is unavailable.

## Pages Updated
- [[Graph-Layout-Algorithms]] — tree layout details
- [[GraphContainer]] — fallback usage context
