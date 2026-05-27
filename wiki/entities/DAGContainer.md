---
title: "DAGContainer"
type: entity
confidence: 0.9
sources:
  - graphcanvas/dag_container.py
  - graphcanvas/graph_view.py
last_updated: 2026-05-19
stale: false
tags: [container, dag, public-api]
---

# DAGContainer

## Overview
A minimal specialization of [[GraphContainer]] that narrows the graph type to `networkx.DiGraph`. Contains no additional behavior — its sole purpose is type safety for directed acyclic graphs.

## Key Attributes
- `graph` — Instance(networkx.DiGraph). Overrides parent's Instance(networkx.Graph).

## Relationships
- Subclass of [[GraphContainer]]
- Instantiated by [[GraphView]] when graph.is_directed() is True
- Part of [[Enable-Component-Model]]

## Open Questions
- Name says "DAG" but no acyclicity enforcement at runtime — only the tree_layout function validates this
