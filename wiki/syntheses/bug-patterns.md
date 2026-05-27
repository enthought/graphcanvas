---
title: "Bug Patterns"
type: synthesis
confidence: 0.9
sources:
  - github-issues
  - graphcanvas/graph_container.py
  - graphcanvas/graph_view.py
  - graphcanvas/layout.py
last_updated: 2026-05-19
stale: false
tags: [bugs, patterns, triage]
---

# Bug Patterns

A living record of bugs encountered in graphcanvas, their root causes, and fixes. Used by the `bug-triage` skill to accelerate diagnosis of new issues.

---

### Single-node directed graph crash
- **Issue**: #4
- **Category**: Edge rendering / empty graph
- **Root cause**: `GraphContainer.draw()` computes arrowhead unit vectors on an empty edge array, causing `IndexError: too many indices for array` when `len(vec) == 0`.
- **Fix**: Skip arrowhead drawing when there are no edges (`if len(vec) == 0: return`).
- **Affected component**: [[GraphContainer]]
- **Date**: 2016-08-18

### graph_from_dict KeyError on NetworkX 2.x
- **Issue**: #34
- **Category**: NetworkX API compatibility
- **Root cause**: `graph.nodes()[0]` uses integer indexing on `NetworkX.NodeView`, which is dict-like in NetworkX 2.x+ and does not support positional access.
- **Fix**: Use `next(iter(self.graph.nodes()))` instead of subscript access (line 78). Additionally, `_get_nodes` now returns `list(self.graph.nodes())` so the `nodes` property provides stable list semantics for all consumers.
- **Affected component**: [[GraphView]]
- **Date**: 2022-09-27 (updated 2026-05-19)

### Intermittent test_do_layout failure
- **Issue**: #32
- **Category**: Layout non-determinism
- **Root cause**: Layout algorithms produce floating-point coordinates like `-2.842e-14` instead of exact `0`, which fails `assertGreaterEqual(component.x, 0)`.
- **Fix**: Use approximate comparison (`assertGreaterEqual(component.x, -1e-10)`) or round layout positions to a tolerance.
- **Affected component**: [[GraphContainer]]
- **Date**: 2021-09-10

### pygraphviz not installable
- **Issue**: #14
- **Category**: Dependency/integration
- **Root cause**: `pygraphviz` requires system-level GraphViz headers (`graphviz-dev`) which are not always available. The import is caught with a bare `try/except ImportError` in the module body.
- **Fix**: Improve fallback handling; document system dependency; add CI matrix entries with and without pygraphviz.
- **Affected component**: [[GraphContainer]]
- **Date**: 2018-07-20
