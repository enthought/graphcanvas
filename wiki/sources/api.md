---
title: "api.py — Public API Module"
type: source
confidence: 0.95
sources:
  - graphcanvas/api.py
last_updated: 2026-05-19
stale: false
tags: [api, exports]
---

# api.py — Public API Module

**Date:** 2009-2019 (Enthought, Inc.)

## Summary
The public API entry point for graphcanvas. Re-exports the four primary classes and one utility function that consumers of the library use directly. Acts as a facade that shields users from internal module paths.

## Key Claims
- GraphView and graph_from_dict are the primary user-facing interfaces (confidence: high)
- GraphNodeComponent, GraphContainer, and DAGContainer are exposed for advanced customization (confidence: high)
- No logic lives in this module — pure re-exports (confidence: high)

## Relevance
Defines the public surface area of the library. Any architectural change to what the library exposes must be reflected here.

## Pages Updated
- [[GraphView]] — identified as primary public class
- [[GraphContainer]] — identified as public export
- [[DAGContainer]] — identified as public export
- [[GraphNodeComponent]] — identified as public export
