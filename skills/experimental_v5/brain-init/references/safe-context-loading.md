# Targeted and safe context loading (v5)

Treat the context size as a **soft budget**, not a hard cap. Start with request, installed version policy, active feature decisions and amendments, relevant Brain root index/ADRs/technical source, actual code owners/callers/tests and current Git changes. Do not read unrelated root docs as ceremony. Broaden automatically when the task crosses boundaries, evidence is incomplete, or authoritative sources conflict.

Do not rely solely on a search result, static path map, hash or handoff as proof. Verify exact protocol/technical contracts against original source sections; check actual code when current behavior matters. Never traverse `.brain/.notes/` by default. Reuse context already accurately retained in the session, rather than rereading unchanged long documents.

`brain-update` is manually invoked. During synchronization it uses verified Git deltas, affected root files and dependencies, expanding as necessary rather than blindly rereading the entire root. Keep main/worktree branch provenance correct.
