# MCP — future (PLANNED): packs as callable tools

Goal: an agent buys its own red-team assessment (the x402 endpoint idea) by calling
pack executions as MCP tools, receiving digest-pinned evidence back.

## Planned tools
| Tool | Args | Returns |
|---|---|---|
| `list_packs` | industry? | pack ids + classes + uk_refs |
| `run_pack` | pack_id, target_base | HELD/BREACHED per probe + evidence digest |
| `run_all` | target_base | full verdict table + run file |

Rules: tools execute the same graded packs (no special-casing targets); evidence
format identical to runner output; priced per request when metered via x402.
Transport: stdio first, streamable-http with the endpoint.
