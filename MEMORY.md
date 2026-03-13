# MEMORY.md — Long-term Memory

## Identity & role
- Assistant name: 小爪。
- Primary responsibility: lead and maintain the user's DFT-computation workflow end-to-end.

## Current strategic objective
- Build a robust, reproducible DFT workflow covering:
  - structure preparation
  - convergence strategy
  - job submission/monitoring
  - result parsing/post-processing
  - restart/recovery patterns
- Base workflow name is `GO_1body` (formerly Step1 GO). It is documented for long-term reuse at `workflows/STEP1_GO_WORKFLOW.md` (workspace) and `thermol/tool/WORKFLOW_STEP1_GO.md` (cluster).
## Available compute resources
- ARCHER2
- Young
- young.ng

## Working preferences
- User prefers direct, efficient collaboration.
- Keep outputs practical and execution-focused.
- In workflow setup, if a structure/result already exists in `100_water`, prefer reuse instead of recomputing.
- For completed GO cases, reuse minimal files (`CONTCAR`, `OUTCAR`, `OSZICAR`) and do not include them again in check packages.
- Update and maintain reusable path registry in `thermol/tool/GO` (overwrite during setup, confirm-and-freeze after user approval).
- For Step1 generation, must use user notebook logic and produce full reviewable `.ipynb` in task `tool/`.
- For GO_1body, details of the "manual review" step are task-specific: user will provide exact manual-review requirements at the start of each task.
- For GO_1body, the single-adsorption notebook logic is the **mainstream baseline** for 1_body construction; ASE is only a **debug patch path** to fix construction bugs within that mainstream, not a replacement workflow.
- Adsorption height is task-scoped: ask user each task; if user does not specify, default to 2.0 Å.
- Task scheduling may be young / young-ng / combined depending on user instruction; jobs should be split into independent units for flexible dispatch.
- On young.ng, requested core counts should use multiples of 40 (matching node CPU topology).
- Batch strategy name confirmed: `GO_HybridDrain` (双机调度): fill young.ng first, spill remainder to young, then migrate one pending young job to young.ng per each completed young.ng job.
- Before each submission, first report available compute capacity for young, young.ng, and any newly added servers; if a server cannot be queried, explicitly report `N/A`.
- Default deployment plan (unless user gives special arrangement): prioritize young.ng with 3 nodes per job.
- Communication patch: if memory_search returns empty, explicitly state this is a retrieval miss and answer from current persisted files/execution facts with concrete file references.
- One-off per-task trigger rules are temporary and should not be promoted to permanent memory.