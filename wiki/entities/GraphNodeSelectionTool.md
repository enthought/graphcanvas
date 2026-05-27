---
title: "GraphNodeSelectionTool"
type: entity
confidence: 0.9
sources:
  - graphcanvas/graph_node_selection_tool.py
last_updated: 2026-05-19
stale: false
tags: [tool, interaction, selection]
---

# GraphNodeSelectionTool

## Overview
Opens a traits editor on double-clicked graph nodes. Extends Enable's BaseTool. The simplest of the three interaction tools (20 lines).

## Behavior
1. `normal_left_dclick()` — hit-tests components at click point
2. If node.value is HasTraits → calls `value.edit_traits()`
3. Otherwise → calls `node.edit_traits(kind='livemodal')`

## Relationships
- Attached to [[GraphContainer]] by [[GraphView]]
- Part of [[Interactive-Tools-Pattern]]
- Targets [[GraphNodeComponent]] instances

## Open Questions
- No visual feedback (highlight) on selection
- No multi-select capability
