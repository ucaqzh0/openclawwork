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

## Available compute resources
- ARCHER2
- Young
- young.ng

## Working preferences
- User prefers direct, efficient collaboration.
- Keep outputs practical and execution-focused.
- In workflow setup, if a structure/result already exists in `100_water`, prefer reuse instead of recomputing.
- For completed GO cases, reuse minimal files (`CONTCAR`, `OUTCAR`, `OSZICAR`) and do not include them again in check packages.
- On young-ng GO submissions, use 80 cores per group when requested.