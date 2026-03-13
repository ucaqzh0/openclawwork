# Crayfish_NEB_zzz

> DFT workflow playground for adsorption → NEB, with reusable 1-body standards and dual-cluster scheduling.

## ✨ What this repo focuses on

This repository captures a practical, reproducible workflow for building and running **GO_1body** adsorption tasks, then preparing clean inputs for later NEB work.

Core goals:
- Standardized structure generation
- Stable submission strategy across **young** + **young.ng**
- Reusable rules that reduce rework and geometry mistakes

---

## 🧭 Key Concepts

### GO_1body
Baseline single-adsorbate workflow (formerly Step1 GO), including:
- structure construction
- submission / monitoring
- check-package export
- reuse policy for completed cases

### GO_HybridDrain（双机调度）
A dual-cluster batching strategy:
1. Fill **young.ng** first (preferred throughput)
2. Spill remaining jobs to **young**
3. When one ng job finishes, migrate one pending young job to ng

---

## 📁 Important Files

- `workflows/STEP1_GO_WORKFLOW.md`  
  Authoritative SOP and scheduling rules for GO_1body.

- `workflows/GO_1body_builder_ase.py`  
  Builder-side rule spec using ASE molecule sources (CO / CHO / COOH logic).

- `MEMORY.md`  
  Long-term distilled decisions and stable operating preferences.

- `memory/*.md`  
  Day-level execution notes and incremental updates.

---

## 🧪 Modeling Rules (current)

- Adsorption sites: `top / bridge / hollow`
- `bridge` = midpoint of **adjacent** surface Cu atoms
- For test set: support `parallel` and `vertical` orientations
- C-anchored placement rules supported for CO / CHO / COOH test generation

---

## 🖥️ Cluster Rules

### young.ng (Slurm)
- Core count should be a multiple of **40**
- Recommended batch template: **3 nodes / 120 cores** per job

### young (SGE/SEG)
- Recommended template: **128 cores** (2 full nodes)

---

## 🔁 Reuse Policy

For completed reusable GO cases, only carry minimal files:
- `CONTCAR`
- `OUTCAR`
- `OSZICAR`

Avoid unnecessary heavy file duplication.

---

## 📌 Status

This repo is actively iterated as workflow rules are validated in production runs.

If you use this workflow, follow the SOP first, then tune per-task parameters.
