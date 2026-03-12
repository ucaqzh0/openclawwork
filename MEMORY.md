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
- Task scheduling may be young / young-ng / combined depending on user instruction; jobs should be split into independent units for flexible dispatch.
- One-off per-task trigger rules are temporary and should not be promoted to permanent memory.