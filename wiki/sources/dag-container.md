---
title: "dag_container.py — DAGContainer"
type: source
confidence: 0.95
sources:
  - graphcanvas/dag_container.py
last_updated: 2026-05-19
stale: false
tags: [container, dag]
---

# dag_container.py — DAGContainer

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
A minimal specialization of GraphContainer that constrains the graph type to `networkx.DiGraph`. Only 15 lines. The only override is the `graph` trait declaration using `Instance(networkx.DiGraph)` instead of `Instance(networkx.Graph)`.

## Key Claims
- DAGContainer is a GraphContainer subclass with no additional behavior (confidence: high)
- Sole purpose is type narrowing: ensures the graph is a DiGraph (confidence: high)

## Relevance
Demonstrates the inheritance pattern. GraphView uses this for directed graphs. Minimal code but architecturally important for type safety.

## Pages Updated
- [[DAGContainer]] — primary documentation source
- [[GraphContainer]] — parent class relationship
